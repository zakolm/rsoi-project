from django.contrib import admin
from .models import Rentals, Devices, RentalDevices


# Register your models here.
@admin.register(Rentals)
class RentalAdmin(admin.ModelAdmin):
    pass


@admin.register(Devices)
class DeviceAdmin(admin.ModelAdmin):
    pass


@admin.register(RentalDevices)
class RentalDevicesAdmin(admin.ModelAdmin):
    pass
