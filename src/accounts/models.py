"""Accounts Models"""
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class BaseProfile(models.Model):
    """BaseProfile used by VolunteerProfile, ClientProfile, ClientDeliveryProfile"""

    user = models.OneToOneField(User, primary_key=True)
    daytime_phone_number = PhoneNumberField("Daytime Phone Number", blank=True, null=True)
    home_phone_number = PhoneNumberField("Home Phone Number", blank=True, null=True)
    cell_phone_number = PhoneNumberField("Cell Number", blank=True, null=True)
    zip_code = models.CharField("Zip Code", max_length=20, blank=True, null=True)
    state = models.CharField("State", max_length=20, blank=True, null=True)
    house_number_street_name = models.CharField("House Number Street Name", max_length=20, blank=True, null=True)
    city = models.CharField("City", max_length=20, blank=True, null=True)

    class Meta:
        abstract = True
