from django.test import TestCase
from django.urls import reverse
from .models import Reservation
import datetime

# Basic test coverage for the home page and reservation creation
class BasicTests(TestCase):
    def test_home_page_status_code(self):
        """
        Ensure the home page (index) returns a 200 status code.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_create_reservation(self):
        """
        Test that a reservation can be created successfully.
        """
        reservation = Reservation.objects.create(
            name="Test User",
            email="test@example.com",
            date=datetime.date(2025, 12, 31),
            time=datetime.time(18, 0),
            party_size=4,
            seating_type='TABLE'
        )
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(reservation.name, "Test User")
