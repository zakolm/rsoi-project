from .models import Rentals, Devices, RentalDevices


def serialize_rental(rental: Rentals) -> dict:
    return {
        'id': rental.id,
        'rentalUid': rental.rental_uid,
        'name': rental.name,
        'city': rental.city,
        'address': rental.address
    }


def serialize_device(device: Devices) -> dict:
    return {
        'deviceUid': device.device_uid,
        'name': device.name,
        'brand': device.brand,
        'condition': device.condition
    }


def serialize_allInfoDevice(device: Devices) -> dict:
    return {
        'id': device.id,
        'deviceUid': device.device_uid,
        'name': device.name,
        'brand': device.brand,
        'condition': device.condition
    }


def serialize_rentalDevices(rd: RentalDevices) -> dict:
    return {
        'avaiblableCount': rd.available_count
    }
