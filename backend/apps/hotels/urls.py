from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, RoomViewSet

router = DefaultRouter()
router.register(r'hotels', HotelViewSet, basename='hotel')
router.register(r'rooms', RoomViewSet, basename='room')

urlpatterns = router.urls
