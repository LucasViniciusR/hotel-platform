from rest_framework import viewsets
from .models import Hotel, Room
from .serializers import HotelSerializer, RoomSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsAdminOrReadOnly

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_pk')
        return Room.objects.filter(hotel_id=hotel_id)