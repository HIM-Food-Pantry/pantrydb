"""Delivery Client Models"""
from django.db import models

from accounts.models import BaseProfile


class DeliveryClientProfile(BaseProfile):
    """Delivery Client Profile"""

    drivers_licence = models.CharField("Drivers Licence Number", max_length=20, blank=True, null=True)
