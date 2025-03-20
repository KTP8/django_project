"""
F-3C: CRUD Operations Implementation
This form is used for creating/updating a reservation.
Only essential fields are exposed to the user. Additional password form for reservation list access.

"""

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Reservation
import datetime

class ReservationForm(forms.ModelForm):
    # Adding validators for party size directly in the form to ensure the input is controlled before hitting the views.
    party_size = forms.IntegerField(
        validators=[
            MinValueValidator(1, "At least one person must be included in the reservation."),
            MaxValueValidator(8, "Maximum party size is 8.")
        ],
        help_text="Enter a number from 1 to 8."
    )
    date = forms.DateField(
        widget=forms.SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
            # Limiting the date picker to only allow dates 6 weeks from the current date
            limit_choices_to={
                'min': datetime.date.today,
                'max': lambda: datetime.date.today() + datetime.timedelta(weeks=6)
            }
        ),
        help_text="Select a date within the next 6 weeks."
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        help_text="Select a time between 11:00 AM and 10:00 PM in 30-minute increments.",
        validators=[
            MinValueValidator(datetime.time(11, 0), "Booking time starts at 11:00 AM."),
            MaxValueValidator(datetime.time(22, 0), "Booking time ends at 10:00 PM.")
        ]
    )

    class Meta:
        model = Reservation
        fields = ['name', 'email', 'date', 'time', 'party_size', 'special_requests']

class PasswordForm(forms.Form):
    # A simple form for owner authentication to view reservation details.
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Enter Password"
    )