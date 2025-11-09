from rest_framework import serializers
from .models import Reservation
from apps.hotels.models import Room


class ReservationSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    class Meta:
        model = Reservation
        fields = ['id', 'room', 'check_in', 'check_out', 'status']
