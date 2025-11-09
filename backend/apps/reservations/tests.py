from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch

from apps.users.models import User
from apps.hotels.models import Hotel, Room
from apps.reservations.models import Reservation
from apps.reservations.tasks import cleanup_expired_reservations

class ReservationBaseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass", role="client")
        self.hotel = Hotel.objects.create(name="Hotel A")
        self.room = Room.objects.create(hotel=self.hotel, number="101", type="single", price=100)

    def test_is_active_confirmed_future_checkout(self):
        reservation = Reservation.objects.create(
            user=self.user,
            room=self.room,
            check_in=timezone.now().date(),
            check_out=timezone.now().date(),
            status='confirmed'
        )
        self.assertTrue(reservation.is_active())

    def test_cleanup_expired_reservations(self):
        today = timezone.now().date()
        pending = Reservation.objects.create(
            user=self.user,
            room=self.room,
            check_in=today.replace(day=today.day - 1),
            check_out=today,
            status='pending'
        )
        confirmed = Reservation.objects.create(
            user=self.user,
            room=self.room,
            check_in=today.replace(day=today.day - 2),
            check_out=today.replace(day=today.day - 1),
            status='confirmed'
        )

        result = cleanup_expired_reservations()

        pending.refresh_from_db()
        confirmed.refresh_from_db()

        self.assertEqual(pending.status, 'cancelled')
        self.assertEqual(confirmed.status, 'completed')
        self.assertEqual(result['cancelled'], 1)
        self.assertEqual(result['completed'], 1)

class ReservationViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass", role="client")
        self.hotel = Hotel.objects.create(name="Hotel A")
        self.room = Room.objects.create(hotel=self.hotel, number="101", type="single", price=100)

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    @patch("apps.reservations.tasks.send_reservation_confirmation.delay")
    def test_create_reservation_success(self, mock_task):
        data = {
            "room": self.room.id,
            "check_in": "2025-11-10",
            "check_out": "2025-11-12"
        }
        response = self.client.post("/api/reservations/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reservation = Reservation.objects.first()
        self.assertEqual(reservation.status, "confirmed")
        mock_task.assert_called_once_with(reservation.id)
