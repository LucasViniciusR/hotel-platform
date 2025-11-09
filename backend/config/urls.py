from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from apps.hotels.views import HotelViewSet, RoomViewSet
from apps.reservations.views import ReservationViewSet

router = routers.DefaultRouter()
router.register(r'hotels', HotelViewSet, basename='hotel')
router.register(r'reservations', ReservationViewSet, basename='reservation')

hotels_router = routers.NestedDefaultRouter(router, r'hotels', lookup='hotel')
hotels_router.register(r'rooms', RoomViewSet, basename='hotel-rooms')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/', include(router.urls)),
    path('api/', include(hotels_router.urls)),
]
