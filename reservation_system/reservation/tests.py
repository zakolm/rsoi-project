import datetime
import json
from typing import List

from django.test import TestCase, Client

from .models import Reservation
from .serializers import serialize_reservation


# Create your tests here.
class TestReservation(TestCase):
    pass
