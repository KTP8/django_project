"""
F-3B: Database Schema & Models Design
This file defines the Reservation model used for restaurant bookings.
It includes seating_type to distinguish between TABLE and COUNTER seating,
and a cancel_token to allow customers to cancel their booking via email.
"""

from django.db import models
from django.utils.crypto import get_random_string

class Reservation(models.Model):
    name = models.CharField(max_length=100)  # Diner's name
    email = models.EmailField()  # Diner's contact email
    date = models.DateField()  # Booking date
    time = models.TimeField()  # Booking time (must be one of our allowed 2-hour slots)
    party_size = models.IntegerField()  # Number of people in the party (max 8)
    special_requests = models.TextField(blank=True)  # Optional extra notes
    created_on = models.DateTimeField(auto_now_add=True)  # Auto-generated timestamp
    seating_type = models.CharField(max_length=20, blank=True)  # "TABLE SEATING" or "COUNTER SEATING"
    cancel_token = models.CharField(max_length=50, blank=True)  # Unique token for cancellation link

    def save(self, *args, **kwargs):
        # Generate a cancellation token if not present
        if not self.cancel_token:
            self.cancel_token = get_random_string(12)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reservation for {self.name} on {self.date} at {self.time}"
