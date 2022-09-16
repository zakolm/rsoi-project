from .models import Reservation


def serialize_reservation(reservation: Reservation) -> dict:
    return {
        'id': reservation.id,
        'reservationUid': str(reservation.reservation_uid),
        'username': reservation.username,

        'deviceUid': str(reservation.device_uid),
        'rentalUid': reservation.rental_uid,

        'status': reservation.status,
        'startDate': str(reservation.start_date),
        'tillDate': str(reservation.till_date),

    }
