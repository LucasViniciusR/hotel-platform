from rest_framework import serializers
from .models import Reservation
from apps.hotels.models import Room


class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['room', 'check_in', 'check_out']


class ReservationSerializer(serializers.ModelSerializer):
    room = serializers.StringRelatedField()

    class Meta:
        model = Reservation
        fields = ['id', 'room', 'check_in', 'check_out', 'status']
