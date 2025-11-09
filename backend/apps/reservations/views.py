from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.reservations.models import Reservation
from apps.reservations.serializers import ReservationSerializer
from apps.reservations.tasks import send_reservation_confirmation


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().select_related('user', 'room')
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.role in ('admin', 'staff'):
            return self.queryset
        return self.queryset.filter(user=user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = serializer.validated_data['room']
        check_in = serializer.validated_data['check_in']
        check_out = serializer.validated_data['check_out']

        overlap = Reservation.objects.filter(
            status__in=['pending', 'confirmed'],
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).exists()

        if overlap:
            raise ValidationError("This room is already booked for the selected dates.")

        reservation = serializer.save(user=request.user, status='confirmed')

        send_reservation_confirmation.delay(reservation.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
