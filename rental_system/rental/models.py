from django.db import models


# Create your models here.
class Rentals(models.Model):
    class Meta:
        db_table = 'rental.rentals'
        verbose_name = 'Рентал'
        verbose_name_plural = 'Ренталы'

    id = models.AutoField(
        primary_key=True
    )
    rental_uid = models.UUIDField(
        unique=True,
        null=False,
        editable=False,
        verbose_name='UID рентала'
    )
    name = models.CharField(
        null=False,
        max_length=80,
        verbose_name='Название рентала'
    )
    city = models.CharField(
        null=False,
        max_length=255,
        verbose_name='Город рентала'
    )
    address = models.CharField(
        null=False,
        max_length=255,
        verbose_name='Адрес рентала'
    )
    picture = models.ImageField(
        upload_to='profile_pictures',
        null=True,
        verbose_name='Фото рентала',
    )

    """def id(self):
        return self.pk"""


class Devices(models.Model):
    class Meta:
        db_table = 'rental.devices'
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'

    id = models.AutoField(
        primary_key=True
    )
    device_uid = models.UUIDField(
        unique=True,
        null=False,
        verbose_name='UID устройства'
    )
    name = models.CharField(
        null=False,
        max_length=255,
        verbose_name='Название устройства'
    )
    brand = models.CharField(
        max_length=255,
        verbose_name='Фирма устройства'
    )
    condition = models.CharField(
        max_length=20,
        default='EXCELLENT',
        verbose_name='Состояние',
        choices=[('EXCELLENT', 'ОТЛИЧНОЕ'),
                 ('GOOD', 'ХОРОШЕЕ'),
                 ('BAD', 'ПЛОХОЕ')]
    )
    picture = models.ImageField(
        upload_to='profile_pictures',
        null=True,
        verbose_name='Фото устройства',
    )

    """def id(self):
        return self.pk"""


class RentalDevices(models.Model):
    class Meta:
        db_table = 'rental.rental_devices'
        verbose_name = 'Рентал - Устройство'
        verbose_name_plural = 'Ренталы - Устройства'

    device_id = models.ForeignKey(
        Devices,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Id устройства'
    )
    rental_id = models.ForeignKey(
        Rentals,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Id рентала'
    )
    available_count = models.IntegerField(
        null=False,
        verbose_name='Доступное количество книг'
    )
