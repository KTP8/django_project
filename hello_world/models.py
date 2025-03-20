"""
F-3B: Database Schema & Models Design
This file defines the Reservation model used for restaurant bookings.
It includes seating_type to distinguish between TABLE and COUNTER seating,
and a cancel_token to allow customers to cancel their booking via email.
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

class Reservation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    party_size = models.PositiveIntegerField()
    seating_type = models.CharField(max_length=10, choices=[('TABLE', 'Table Seating'), ('COUNTER', 'Counter Seating')])
    status = models.CharField(max_length=20, default='AWAITING', choices=[('CONFIRMED', 'Booking Confirmed'), ('CANCELLED', 'Booking Cancelled'), ('AWAITING', 'Awaiting Response')])

    def clean(self):
        if not (datetime.time(11, 00) <= self.time <= datetime.time(22, 00)):
            raise ValidationError("Bookings can only be made between 11 AM and 10 PM.")
        if self.date > timezone.now().date() + datetime.timedelta(weeks=6):
            raise ValidationError("Bookings can only be made up to six weeks in advance.")
        existing_booking = Reservation.objects.filter(date=self.date, time=self.time, seating_type=self.seating_type)
        if existing_booking.exists():
            raise ValidationError("This slot is already booked.")

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time} - {self.status}"
