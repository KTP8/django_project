"""
F-3: Advanced Booking Logic, Authentication, and Email Integration
This file extends our booking view to include:
- Time slot and date validations
- Seating assignment logic
- Duplicate booking detection
- Email notification with cancellation link
- Owner-restricted reservation views using a simple password ("boss")
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta, time as dt_time
from .models import Reservation
from .forms import ReservationForm

# Define allowed booking times (2-hour slots)
ALLOWED_TIMES = [dt_time(11, 0), dt_time(13, 0), dt_time(15, 0), dt_time(17, 0), dt_time(19, 0)]

def index(request):
    # Existing home page view
    return render(request, 'hello_world/index.html')

def menu(request):
    # New menu page view
    return render(request, 'hello_world/menu.html')

def booking(request):
    """
    Booking view for customers.
    Validates booking times, date limits, party size, and seating availability.
    Also checks for duplicate bookings and sends an email confirmation.
    """
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            chosen_date = cd['date']
            chosen_time = cd['time']
            party_size = cd['party_size']
            diner_email = cd['email']
            
            # Validate booking time: must be one of the allowed slots
            if chosen_time not in ALLOWED_TIMES:
                error = "Bookings are only available at fixed slots: 11:00, 13:00, 15:00, 17:00, and 19:00."
                return render(request, 'hello_world/booking.html', {'form': form, 'error': error})
            
            # Validate booking date: within 6 weeks from now
            six_weeks_from_now = datetime.now().date() + timedelta(weeks=6)
            if chosen_date > six_weeks_from_now:
                error = "Sorry, we don't take bookings more than 6 weeks ahead."
                return render(request, 'hello_world/booking.html', {'form': form, 'error': error})
            
            # Validate party size: max 8
            if party_size > 8:
                error = "Maximum party size is 8."
                return render(request, 'hello_world/booking.html', {'form': form, 'error': error})
            
            # Check for duplicate booking on same day using same email
            existing_booking = Reservation.objects.filter(email=diner_email, date=chosen_date)
            if existing_booking.exists() and not request.POST.get('email_confirmed'):
                message = f"You already have a booking on {existing_booking.first().date} at {existing_booking.first().time}. Are you sure you'd like to book again?"
                return render(request, 'hello_world/booking.html', {'form': form, 'confirm_email': True, 'message': message})
            
            # Determine default seating assignment based on party size
            #   - 1-2: Table seating for 2
            #   - 3-4: Table seating for 4
            #   - 5-6: Table seating for 6
            #   - 7-8: Counter seating
            if party_size <= 2:
                default_seating = "TABLE SEATING"
                table_category = '2'
                max_available = 6  # 6 tables for 2 available
            elif party_size <= 4:
                default_seating = "TABLE SEATING"
                table_category = '4'
                max_available = 10  # 10 tables for 4 available
            elif party_size <= 6:
                default_seating = "TABLE SEATING"
                table_category = '6'
                max_available = 10  # 10 tables for 6 available
            else:
                default_seating = "COUNTER SEATING"
            
            # Override with user seating choice if provided
            user_seating_choice = request.POST.get('seating_choice', None)  # 'table' or 'counter'
            if user_seating_choice:
                if party_size in [7,8] and user_seating_choice == 'table':
                    error = "For parties of 7 or 8, counter seating is required."
                    return render(request, 'hello_world/booking.html', {'form': form, 'error': error})
                else:
                    chosen_seating = "COUNTER SEATING" if user_seating_choice == 'counter' else "TABLE SEATING"
            else:
                chosen_seating = default_seating
            
            # Check availability:
            if chosen_seating == "TABLE SEATING":
                if table_category == '2':
                    current_count = Reservation.objects.filter(date=chosen_date, time=chosen_time, seating_type="TABLE SEATING", party_size__lte=2).count()
                    if current_count >= 6:
                        error = "Only TABLE SEATING for 2 is available at your chosen time."
                        return render(request, 'hello_world/booking.html', {'form': form, 'error': error})
                elif table_category == '4':
                    current_count = Reservation.objects.filter(date=chosen_date, time=chosen_time, seating_type="TABLE SEATING", party_size__range=(3,4)).count()
                    if current_count >= 10:
                        error = "Only TABLE SEATING for 4 is available at your chosen time."
                        return render(request, 'hello_world/booking.html', {'form': form, 'error': error})
                elif table_category == '6':
                    current_count = Reservation.objects.filter(date=chosen_date, time=chosen_time, seating_type="TABLE SEATING", party_size__range=(5,6)).count()
                    if current_count >= 10:
                        error = "Only TABLE SEATING for 6 is available at your chosen time."
                        return render(request, 'hello_world/booking.html', {'form': form, 'error': error})
            elif chosen_seating == "COUNTER SEATING":
                # Sum party sizes for counter seating at this slot
                current_counter = sum([r.party_size for r in Reservation.objects.filter(date=chosen_date, time=chosen_time, seating_type="COUNTER SEATING")])
                if current_counter + party_size > 10:
                    error = "Only COUNTER SEATING is available and it's fully booked for your party size."
                    return render(request, 'hello_world/booking.html', {'form': form, 'error': error})
            
            # Create and save the reservation
            new_reservation = form.save(commit=False)
            new_reservation.seating_type = chosen_seating
            new_reservation.save()
            
            # Send email confirmation with reservation details and cancellation link
            subject = "Your Reservation at La Italia"
            body = (
                f"Hello {new_reservation.name},\n\n"
                "Thank you for booking a table at La Italia.\n\n"
                f"Reservation Details:\nDate: {new_reservation.date}\nTime: {new_reservation.time}\n"
                f"Party Size: {new_reservation.party_size}\nSeating: {new_reservation.seating_type}\n\n"
                f"To cancel your reservation, please visit the following link:\n"
                f"http://127.0.0.1:8000/cancel/{new_reservation.cancel_token}\n\n"
                "We look forward to serving you!\nLa Italia"
            )
            try:
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [new_reservation.email])
            except Exception as e:
                # Log error but do not block the booking
                print(f"Error sending email: {e}")
            
            return render(request, 'hello_world/booking_confirm.html')
        else:
            # If form is invalid, re-render with errors
            return render(request, 'hello_world/booking.html', {'form': form})
    else:
        form = ReservationForm()
        return render(request, 'hello_world/booking.html', {'form': form})

def cancel_reservation(request, token):
    """
    Allows a customer to cancel their reservation via the unique token in the email.
    """
    reservation = Reservation.objects.filter(cancel_token=token).first()
    if not reservation:
        return HttpResponse("Invalid or expired cancellation link.")
    reservation.delete()
    return HttpResponse("Your reservation has been cancelled.")

# Owner-only reservation views (accessed with ?pwd=boss)

def reservation_list(request):
    """
    Displays all reservations on an owner-only dashboard.
    Owner must append ?pwd=boss to the URL.
    """
    if request.GET.get('pwd') != 'boss':
        return HttpResponse("Not authorized. Please add ?pwd=boss to the URL.")
    reservations = Reservation.objects.all().order_by('-date', '-time')
    return render(request, 'hello_world/reservation_list.html', {'reservations': reservations})

def reservation_detail(request, pk):
    """
    Displays details for a single reservation.
    Restricted to owner via ?pwd=boss.
    """
    if request.GET.get('pwd') != 'boss':
        return HttpResponse("Not authorized to view reservation details.")
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'hello_world/reservation_detail.html', {'reservation': reservation})

def reservation_delete(request, pk):
    """
    Allows the owner to delete a reservation.
    Restricted to owner via ?pwd=boss.
    """
    if request.GET.get('pwd') != 'boss':
        return HttpResponse("Not authorized to delete reservations.")
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        reservation.delete()
        return redirect('/reservations?pwd=boss')
    return render(request, 'hello_world/reservation_delete_confirm.html', {'reservation': reservation})
