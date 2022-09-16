import datetime
import json
from typing import List

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse, HttpResponse
from django import views

from .models import Reservation
from .serializers import serialize_reservation


# Create your views here.
class ReservationsView(views.View):
    @staticmethod
    def get(request: WSGIRequest, *args, **kwargs):
        username = request.headers.get('X-User-Name')
        if username is None:
            queryset: List[Reservation] = Reservation.objects.all()
        else:
            queryset: List[Reservation] = Reservation.objects.filter(
                username=username)
        if len(queryset) == 0:
            return HttpResponse('Reservation not found', status=404)
        data = [serialize_reservation(reservation) for reservation in queryset]
        return JsonResponse(data, safe=False)

    @staticmethod
    def post(request, *args, **kwargs):
        headers_dict = request.headers

        # body_unicode = request.body.decode('utf-8')
        body_dict = json.loads(request.body)

        print(kwargs)
        if 'X-User-Name' in headers_dict.keys():
            body_dict['username'] = headers_dict['X-User-Name']

        if request.get_full_path().find('return') > -1:
            queryset: List[Reservation] = Reservation.objects.filter(
                username=body_dict['username'],
                reservation_uid=kwargs['reservationUid']).all()
            if len(queryset) == 0:
                return HttpResponse('Reservation not found', status=404)

            reservation: Reservation = queryset[0]

            status = 'RETURNED'
            if datetime.datetime.strptime(body_dict['date'], '%Y-%m-%d') > \
                    reservation.till_date.replace(tzinfo=None):
                status = 'EXPIRED'

            setattr(reservation, 'status', status)
            reservation.save()
            data = serialize_reservation(reservation)
        else:
            deviceUid = body_dict.get('deviceUid')
            """queryset = Device.objects.filter(id=device_uid).all()
            if len(queryset) == 0:
                return HttpResponse('Device not found', status=404)"""
            rentalUid = body_dict.get('rentalUid')
            """queryset = Rental.objects.filter(id=rental_uid).all()
            if len(queryset) == 0:
                return HttpResponse('Rental not found', status=404)"""
            tillDate = body_dict.get('tillDate')

            reservation = {'device_uid': deviceUid, 'rental_uid': rentalUid,
                           'username': body_dict['username'],
                           'till_date': tillDate, 'start_date':
                               datetime.datetime.now().strftime('%Y-%m-%d'),
                           'status': 'RENTED'}

            new_reservation = Reservation(**reservation)
            new_reservation.save()

            data = serialize_reservation(new_reservation)

        return JsonResponse(data, status=201, safe=False)
