from django.urls import path
from .views import ReservationsView

urlpatterns = [
    path('reservations/<uuid:reservationUid>/return',
                                                   ReservationsView.as_view()),
    path('reservations', ReservationsView.as_view()),
]
