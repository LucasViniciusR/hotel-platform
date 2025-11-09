from rest_framework import serializers
from .models import Hotel, Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'number', 'type', 'price', 'is_available']

class HotelSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'description', 'rooms']
