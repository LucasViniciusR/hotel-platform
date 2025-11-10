from django.contrib import admin
from .models import Room, Hotel, RoomImage


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'description')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'type', 'price', 'is_available')
    inlines = [RoomImageInline]
