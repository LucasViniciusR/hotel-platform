from django.contrib import admin
from .models import Room, Hotel


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'description')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'type', 'price', 'is_available')
