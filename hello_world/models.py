"""
F-3B: Database Schema & Models Design
This file defines the Reservation model used for restaurant bookings.
It includes seating_type to distinguish between TABLE and COUNTER seating,
and a cancel_token to allow customers to cancel their booking via email.
"""

import uuid
import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Reservation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    party_size = models.PositiveIntegerField()
    seating_type = models.CharField(
        max_length=10,
        choices=[
            ('TABLE', 'Table Seating'),
            ('COUNTER', 'Counter Seating')
        ]
    )
    status = models.CharField(
        max_length=20,
        default='AWAITING',
        choices=[
            ('CONFIRMED', 'Booking Confirmed'),
            ('CANCELLED', 'Booking Cancelled'),
            ('AWAITING', 'Awaiting Response'),
            ('DUPLICATE', 'Multiple Bookings - Contact')
        ]
    )
    # Added field for unique cancellation token
    cancel_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def clean(self):
        # Ensure the booking time is within the operational hours
        if not (datetime.time(11, 0) <= self.time <= datetime.time(22, 0)):
            raise ValidationError("Bookings can only be made between 11 AM and 10 PM.")
        
        # Ensure the booking is no more than six weeks out
        if self.date > timezone.now().date() + datetime.timedelta(weeks=6):
            raise ValidationError("Bookings can only be made up to six weeks in advance.")
        
        # Check if the slot is already booked
        existing_booking = Reservation.objects.filter(
            date=self.date,
            time=self.time,
            seating_type=self.seating_type
        )
        if existing_booking.exists():
            raise ValidationError("This slot is already booked.")

    def __str__(self):
        return f"{self.name} - {self.date.strftime('%Y-%m-%d')} at {self.time.strftime('%H:%M')} - {self.status}"
