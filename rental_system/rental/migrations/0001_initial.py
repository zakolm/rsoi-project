# Generated by Django 4.1.1 on 2022-09-16 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('device_uid', models.UUIDField(unique=True, verbose_name='UID устройства')),
                ('name', models.CharField(max_length=255, verbose_name='Название устройства')),
                ('brand', models.CharField(max_length=255, verbose_name='Фирма устройства')),
                ('condition', models.CharField(choices=[('EXCELLENT', 'ОТЛИЧНОЕ'), ('GOOD', 'ХОРОШЕЕ'), ('BAD', 'ПЛОХОЕ')], default='EXCELLENT', max_length=20, verbose_name='Состояние')),
            ],
            options={
                'verbose_name': 'Устройство',
                'verbose_name_plural': 'Устройства',
                'db_table': 'rental.devices',
            },
        ),
        migrations.CreateModel(
            name='Rentals',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rental_uid', models.UUIDField(editable=False, unique=True, verbose_name='UID рентала')),
                ('name', models.CharField(max_length=80, verbose_name='Название рентала')),
                ('city', models.CharField(max_length=255, verbose_name='Город рентала')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес рентала')),
            ],
            options={
                'verbose_name': 'Рентал',
                'verbose_name_plural': 'Ренталы',
                'db_table': 'rental.rentals',
            },
        ),
        migrations.CreateModel(
            name='RentalDevices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_count', models.IntegerField(verbose_name='Доступное количество книг')),
                ('device_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rental.devices', verbose_name='Id устройства')),
                ('rental_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rental.rentals', verbose_name='Id рентала')),
            ],
            options={
                'verbose_name': 'Рентал - Устройство',
                'verbose_name_plural': 'Ренталы - Устройства',
                'db_table': 'rental.rental_devices',
            },
        ),
    ]
