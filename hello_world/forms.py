"""
F-3C: CRUD Operations Implementation
This form is used for creating/updating a reservation.
Only essential fields are exposed to the user.
"""

from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'date', 'time', 'party_size', 'special_requests']
