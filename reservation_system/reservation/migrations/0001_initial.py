# Generated by Django 4.1.1 on 2022-09-16 21:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reservation_uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UID брони')),
                ('username', models.CharField(max_length=80, verbose_name='Имя пользователя')),
                ('device_uid', models.UUIDField(editable=False, verbose_name='UID устройства')),
                ('rental_uid', models.UUIDField(editable=False, null=True, verbose_name='UID рентала')),
                ('status', models.CharField(choices=[('RENTED', 'АРЕНДОВАНО'), ('RETURNED', 'ВОЗВРАЩЕНО'), ('EXPIRED', 'ИСТЕКЛО')], max_length=20, verbose_name='Статус')),
                ('start_date', models.DateTimeField(verbose_name='Дата начала')),
                ('till_date', models.DateTimeField(verbose_name='До даты')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Бронирования',
                'db_table': 'reservations.reservation',
            },
        ),
    ]
