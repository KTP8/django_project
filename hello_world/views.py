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

# Dynamic allowed booking times from 11:00 to 22:00 at 30-minute intervals
ALLOWED_TIMES = [dt_time(hour=h, minute=m) for h in range(11, 23) for m in (0, 30)]

def index(request):
    # Home page view
    return render(request, 'hello_world/index.html')

def menu(request):
    # Menu page view
    return render(request, 'hello_world/menu.html')

def booking(request):
    """
    Handles customer bookings with dynamic validations and sends email confirmations.
    """
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            chosen_date = cd['date']
            chosen_time = cd['time']
            party_size = cd['party_size']
            diner_email = cd['email']

            # Time validation against allowed slots
            if chosen_time not in ALLOWED_TIMES:
                return render(request, 'hello_world/booking.html', {
                    'form': form,
                    'error': "Select a valid booking time between 11:00 AM and 10:00 PM in 30-minute increments."
                })

            # Booking date validation for up to six weeks ahead
            if chosen_date > datetime.now().date() + timedelta(weeks=6):
                return render(request, 'hello_world/booking.html', {
                    'form': form,
                    'error': "Bookings can only be made up to six weeks in advance."
                })

            # Party size validation with maximum limit
            if party_size > 8:
                return render(request, 'hello_world/booking.html', {
                    'form': form,
                    'error': "The maximum party size is 8."
                })

            # Duplicate booking check for the same email within 5 days window
            existing_booking = Reservation.objects.filter(
                email=diner_email,
                date__range=[chosen_date - timedelta(days=5), chosen_date + timedelta(days=5)]
            )
            if existing_booking.exists():
                return render(request, 'hello_world/booking.html', {
                    'form': form,
                    'error': "Multiple bookings detected. Please contact support."
                })

            # Assign seating based on party size
            if party_size >= 7:
                chosen_seating = "COUNTER"
            else:
                chosen_seating = "TABLE"

            # Create and save the reservation
            new_reservation = form.save(commit=False)
            new_reservation.seating_type = chosen_seating
            new_reservation.save()

            # Email confirmation with details and cancellation link
            send_mail(
                'Booking Confirmation - La Italia',
                (
                    f"Hello {new_reservation.name},\n\n"
                    f"Thank you for your reservation at La Italia.\n\n"
                    f"Details:\n"
                    f"Date: {new_reservation.date}\n"
                    f"Time: {new_reservation.time}\n"
                    f"Party Size: {new_reservation.party_size}\n"
                    f"Seating: {new_reservation.seating_type}\n\n"
                    f"To cancel your reservation, please follow this link: "
                    f"http://127.0.0.1:8000/cancel/{new_reservation.cancel_token}\n\n"
                    "We look forward to welcoming you!"
                ),
                settings.DEFAULT_FROM_EMAIL,
                [diner_email],
                fail_silently=False,
            )
            return render(request, 'hello_world/booking_confirm.html', {
                'message': 'Booking successful! Check your email for confirmation.'
            })
        else:
            return render(request, 'hello_world/booking.html', {'form': form})
    else:
        form = ReservationForm()
        return render(request, 'hello_world/booking.html', {'form': form})

def reservation_list(request):
    """
    Owner-only view for reservation lists accessed via a password form.
    """
    form = PasswordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid() and form.cleaned_data['password'] == 'boss':
        reservations = Reservation.objects.all().order_by('-date', '-time')
        return render(request, 'hello_world/reservation_list.html', {
            'reservations': reservations,
            'form': form
        })
    return render(request, 'hello_world/password_entry.html', {'form': form})

def reservation_detail(request, pk):
    """
    Detail view for individual reservations, accessed by the owner with a password.
    """
    form = PasswordForm(request.GET or None)
    if form.is_valid() and form.cleaned_data['password'] == 'boss':
        reservation = get_object_or_404(Reservation, pk=pk)
        return render(request, 'hello_world/reservation_detail.html', {'reservation': reservation})
    return HttpResponse("Unauthorized access. Please enter the correct password.")

def reservation_delete(request, pk):
    """
    Allows the owner to delete a reservation, accessed via password.
    """
    form = PasswordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid() and form.cleaned_data['password'] == 'boss':
        reservation = get_object_or_404(Reservation, pk=pk)
        reservation.delete()
        return redirect('reservation_list')
    return render(request, 'hello_world/reservation_delete_confirm.html', {'form': form})

def cancel_reservation(request, token):
    """
    Allows customers to cancel their reservations using a unique cancellation token.
    """
    reservation = get_object_or_404(Reservation, cancel_token=token)
    if request.method == 'GET':
        reservation.delete()
        return HttpResponse("Your reservation has been cancelled successfully. We hope to see you another time!")
