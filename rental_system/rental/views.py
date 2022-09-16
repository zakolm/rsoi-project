import json
import uuid
from typing import List

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import serialize_rental, serialize_device, \
    serialize_allInfoDevice, serialize_rentalDevices

from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django import views
from rest_framework.request import Request

from .models import Rentals, Devices, RentalDevices


# Create your views here.
class RentalViewSet(views.View):
    def get(self, request: WSGIRequest, *args, **kwargs):
        response = ""
        city = request.GET.get('city', None)
        page_number = request.GET.get('page', None)
        page_size = request.GET.get('size', None)
        if city is not None:
            if page_number is not None or page_size is not None:
                if page_number is not None and page_size is not None:
                    page_number = int(page_number)
                    page_size = int(page_size)
                    if page_size < 1:
                        page_size = 1
                    if page_number < 1:
                        page_number = 1
                    queryset: List[Rentals] = Rentals.objects.filter(
                        city=city).all()
                    pagination = Paginator(queryset, page_size)
                    queryset = pagination.get_page(page_number)
                    if len(queryset) == 0:
                        return HttpResponse('Rental not found', status=404)
                else:
                    queryset: List[Rentals] = Rentals.objects.filter(
                        city=city).all()
                    if len(queryset) == 0:
                        return HttpResponse('Rental not found', status=404)
                data = [serialize_rental(rental) for rental in queryset]
                response = {
                    'page': page_number,
                    'pageSize': page_size,
                    'totalElements': Rentals.objects.all().count(),
                    'items': data
                }
            else:
                queryset: List[Rentals] = Rentals.objects.filter(
                    city=city).all()
                if len(queryset) == 0:
                    return HttpResponse('Rental not found', status=404)
                data = [serialize_rental(rental) for rental in queryset]
                response = data

        if kwargs.get('rentalUid') is not None:
            rentalUid = kwargs['rentalUid']
            queryset_rental: List[Rentals] = Rentals.objects.all()
            queryset = list()
            for el in queryset_rental:
                if el.rental_uid == rentalUid:
                    queryset.append(el)
            if len(queryset) == 0:
                return HttpResponse('Rental not found', status=404)
            data = serialize_rental(queryset[0])
            response = data

        return JsonResponse(response, safe=False)


class DeviceViewSet(views.View):
    def get(self, request: WSGIRequest, *args, **kwargs):
        showAll = request.GET.get('showAll', None)
        page_number = request.GET.get('page', None)
        page_size = request.GET.get('size', None)
        response = ""
        if kwargs.get('deviceUid') is not None:
            deviceUid = kwargs['deviceUid']
            queryset_device: List[Devices] = Devices.objects.all()
            queryset = list()
            for el in queryset_device:
                if el.device_uid == deviceUid:
                    queryset.append(el)
            if len(queryset) == 0:
                return HttpResponse('Device not found', status=404)
            data = serialize_allInfoDevice(queryset[0])
            response = data
        elif request.get_full_path().find('devices') > -1:
            rentalUid = kwargs['rentalUid']

            queryset_rental: List[Rentals] = Rentals.objects.all()
            queryset = list()
            for el in queryset_rental:
                if el.rental_uid == rentalUid:
                    queryset.append(el)
            if len(queryset) == 0:
                return HttpResponse('Rental not found', status=404)

            if showAll:
                queryset_lb: List[RentalDevices] = RentalDevices.objects.filter(
                    rental_id=queryset[0].id).all()
            else:
                queryset_lb: List[RentalDevices] = RentalDevices.objects.filter(
                    rental_id=queryset[0].id).exclude(
                    available_count=0).all()

            queryset_device = list()
            for idx, el in enumerate(queryset_lb):
                dct = serialize_device(el.device_id)
                queryset_device.append(dct)
                queryset_device[idx]['available_count'] = el.available_count

            if page_number is not None or page_size is not None:
                if page_number is not None and page_size is not None:
                    page_number = int(page_number)
                    page_size = int(page_size)
                    if page_size < 1:
                        page_size = 1
                    if page_number < 1:
                        page_number = 1

                    pagination = Paginator(queryset_device, page_size)
                    queryset_device = pagination.get_page(page_number)

                data = [device for device in queryset_device]
                response = {
                    'page': page_number,
                    'pageSize': page_size,
                    'totalElements': Rentals.objects.all().count(),
                    'items': data
                }
            else:
                data = [serialize_device(device) for device in queryset_device]
                response = {
                    'page': page_number,
                    'pageSize': page_size,
                    'totalElements': Rentals.objects.all().count(),
                    'items': data
                }

        return JsonResponse(response, safe=False)

    def post(self, request: WSGIRequest, *args, **kwargs):
        body_dict = json.loads(request.body)

        print(body_dict)

        deviceUid = kwargs['deviceUid']
        queryset_device: List[Devices] = Devices.objects.all()

        queryset = list()
        for el in queryset_device:
            if el.device_uid == deviceUid:
                queryset.append(el)
        if len(queryset) == 0:
            return HttpResponse('Device not found', status=404)

        device: Devices = queryset[0]
        setattr(device, 'condition', body_dict.get('condition'))
        device.save()

        data = serialize_device(device)

        return JsonResponse(data, safe=False)


class RentalDevicesViewSet(views.View):
    def get(self, request: WSGIRequest, *args, **kwargs):
        response = ""
        rentalId = request.GET.get('rentalId', None)
        deviceId = request.GET.get('deviceId', None)
        if rentalId is not None and deviceId is not None:
            queryset: List[RentalDevices] = RentalDevices.objects.filter(
                rental_id=rentalId,
                device_id=deviceId).all()
            if len(queryset) == 0:
                return HttpResponse('Rental not found', status=404)
            data = serialize_rentalDevices(queryset[0])
            response = data

        return JsonResponse(response, safe=False)

    def post(self, request: WSGIRequest, *args, **kwargs):
        rentalId = request.GET.get('rentalId', None)
        deviceId = request.GET.get('deviceId', None)
        reservationUid = kwargs.get('reservationUid')
        print(rentalId, deviceId)
        if rentalId is not None and deviceId is not None:
            queryset: List[RentalDevices] = RentalDevices.objects.filter(
                device_id=deviceId,
                rental_id=rentalId).all()
        elif reservationUid is not None:
            queryset: List[RentalDevices] = RentalDevices.objects.filter(
                reservationUid=reservationUid).all()
        else:
            queryset = []

        if len(queryset) > 0:
            rd: RentalDevices = queryset[0]
            print(rd.available_count)
            if request.get_full_path().find('return') > -1:
                availableCount = 0
                if 0 <= rd.available_count <= 99:
                    availableCount = rd.available_count + 1
            else:
                availableCount = 0
                if 0 < rd.available_count <= 100:
                    availableCount = rd.available_count - 1

            setattr(rd, 'available_count', availableCount)
            rd.save()
            data = serialize_rentalDevices(rd)
        else:
            data = None

        return JsonResponse(data, safe=False)
