from django.core.validators import MinValueValidator
from django.db import models

class RoomType(models.TextChoices):
    SINGLE = 'single', 'Single'
    DOUBLE = 'double', 'Double'
    SUITE = 'suite', 'Suite'

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name='rooms')
    number = models.CharField(max_length=10)
    type = models.CharField(max_length=50, choices=RoomType.choices, default=RoomType.SINGLE)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['hotel', 'number'], name='unique_room_per_hotel')
        ]

    def __str__(self):
        return f"{self.hotel.name} - Room {self.number}"
