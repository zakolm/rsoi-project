from django.urls import path

from .views import RentalViewSet, DeviceViewSet, RentalDevicesViewSet


urlpatterns = [
    path('rentals', RentalViewSet.as_view()),
    path('rentals/<uuid:rentalUid>', RentalViewSet.as_view()),
    path('rentals/<uuid:rentalUid>/devices', DeviceViewSet.as_view()),
    path('devices/<uuid:deviceUid>', DeviceViewSet.as_view()),
    path('availableCount', RentalDevicesViewSet.as_view()),
    path('availableCount/return', RentalDevicesViewSet.as_view())
]
