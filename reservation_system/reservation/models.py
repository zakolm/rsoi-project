import uuid

from django.db import models


# Create your models here.
class Reservation(models.Model):
    class Meta:
        db_table = 'reservations.reservation'
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
    id = models.AutoField(
        primary_key=True
    )
    reservation_uid = models.UUIDField(
        unique=True,
        null=False,
        default=uuid.uuid4,
        editable=False,
        verbose_name='UID брони'
    )
    username = models.CharField(
        null=False,
        max_length=80,
        verbose_name='Имя пользователя'
    )
    device_uid = models.UUIDField(
        null=False,
        editable=False,
        verbose_name='UID устройства'
    )
    rental_uid = models.UUIDField(
        null=True,
        editable=False,
        verbose_name='UID рентала'
    )
    status = models.CharField(
        null=False,
        max_length=20,
        verbose_name='Статус',
        choices=[('RENTED', 'АРЕНДОВАНО'),
                 ('RETURNED', 'ВОЗВРАЩЕНО'),
                 ('EXPIRED', 'ИСТЕКЛО')]
    )
    start_date = models.DateTimeField(
        null=False,
        verbose_name='Дата начала'
    )
    till_date = models.DateTimeField(
        null=False,
        verbose_name='До даты'
    )
