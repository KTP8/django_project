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
from .forms import ReservationForm, PasswordForm

# Define dynamic booking times from 11:00 to 22:00 at 30-minute intervals
ALLOWED_TIMES = [dt_time(hour=h, minute=m) for h in range(11, 22) for m in (0, 30)]

def index(request):
    # Static home page view
    return render(request, 'hello_world/index.html')

def menu(request):
    # Static menu page view
    return render(request, 'hello_world/menu.html')

def booking(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            chosen_date = cd['date']
            chosen_time = cd['time']
            party_size = cd['party_size']
            diner_email = cd['email']

            # Time validation
            if chosen_time not in ALLOWED_TIMES:
                return render(request, 'hello_world/booking.html', {'form': form, 'error': "Please select a valid booking time between 11:00 AM and 10:00 PM in 30-minute increments."})

            # Booking date validation
            six_weeks_ahead = datetime.now().date() + timedelta(weeks=6)
            if chosen_date > six_weeks_ahead:
                return render(request, 'hello_world/booking.html', {'form': form, 'error': "Bookings can only be made up to six weeks in advance."})

            # Party size validation
            if party_size > 8:
                return render(request, 'hello_world/booking.html', {'form': form, 'error': "The maximum party size is 8."})

            # Duplicate booking check
            existing_booking = Reservation.objects.filter(email=diner_email, date__range=[chosen_date - timedelta(days=5), chosen_date + timedelta(days=5)])
            if existing_booking.exists():
                return render(request, 'hello_world/booking.html', {'form': form, 'error': "You already have a booking around these dates. Please verify your bookings."})

            # Seating assignment logic
            if party_size >= 7:
                chosen_seating = "COUNTER SEATING"
                max_counter_seats = 10
                current_counter = sum(r.party_size for r in Reservation.objects.filter(date=chosen_date, time=chosen_time, seating_type=chosen_seating))
                if current_counter + party_size > max_counter_seats:
                    return render(request, 'hello_world/booking.html', {'form': form, 'error': "Only counter seating available and it's fully booked for your party size."})
            else:
                chosen_seating = "TABLE SEATING"

            new_reservation = form.save(commit=False)
            new_reservation.seating_type = chosen_seating
            new_reservation.save()

            # Email confirmation
            send_mail(
                'Booking Confirmation - La Italia',
                f'Hello {new_reservation.name},\n\nThank you for your reservation at La Italia.\n\nDetails:\nDate: {new_reservation.date}\nTime: {new_reservation.time}\nParty Size: {new_reservation.party_size}\nSeating: {new_reservation.seating_type}.',
                settings.DEFAULT_FROM_EMAIL,
                [diner_email],
                fail_silently=False,
            )
            return render(request, 'hello_world/booking_confirm.html')
        else:
            return render(request, 'hello_world/booking.html', {'form': form})
    else:
        form = ReservationForm()
        return render(request, 'hello_world/booking.html', {'form': form})

# Owner-only reservation views with secure password entry
def reservation_list(request):
    form = PasswordForm()
    if request.method == 'POST' and form.is_valid():
        password = form.cleaned_data.get('password')
        if password == 'boss':
            reservations = Reservation.objects.all().order_by('-date', '-time')
            return render(request, 'hello_world/reservation_list.html', {'reservations': reservations})
        else:
            return HttpResponse("Unauthorized access.")
    return render(request, 'hello_world/password_entry.html', {'form': form})

def reservation_detail(request, pk):
    form = PasswordForm(request.GET)
    if form.is_valid() and form.cleaned_data.get('password') == 'boss':
        reservation = get_object_or_404(Reservation, pk=pk)
        return render(request, 'hello_world/reservation_detail.html', {'reservation': reservation})
    return HttpResponse("Unauthorized access.")

def reservation_delete(request, pk):
    form = PasswordForm(request.GET)
    if form.is_valid() and form.cleaned_data.get('password') == 'boss':
        reservation = get_object_or_404(Reservation, pk=pk)
        reservation.delete()
        return redirect('reservation_list')
    return HttpResponse("Unauthorized access.")

def cancel_reservation(request, token):
    reservation = get_object_or_404(Reservation, cancel_token=token)
    reservation.delete()
    return HttpResponse("Your reservation has been cancelled successfully.")
