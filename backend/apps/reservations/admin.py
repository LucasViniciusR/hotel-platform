from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'status')
