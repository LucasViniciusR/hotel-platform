from django.db import models
from apps.hotels.models import Room
from apps.users.models import User
from django.conf import settings
from django.utils import timezone


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.room.hotel.name} Room {self.room.number}"

    def is_active(self):
        return self.status == 'confirmed' and self.check_out >= timezone.now().date()
