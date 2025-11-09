from celery import shared_task
from django.core.mail import send_mail
from apps.reservations.models import Reservation

@shared_task
def send_reservation_confirmation(reservation_id):
    try:
        reservation = Reservation.objects.select_related('user', 'room').get(id=reservation_id)
    except Reservation.DoesNotExist:
        return

    subject = f"Reservation Confirmed: Hotel {reservation.room.hotel.name}"
    message = (
        f"Hello {reservation.user.username},\n\n"
        f"Your reservation for {reservation.room.hotel.name}, "
        f"Room {reservation.room.number} from {reservation.check_in} to {reservation.check_out} "
        f"has been confirmed.\n\nThank you!"
    )
    send_mail(subject, message, "no-reply@hotel.com", [reservation.user.email])
