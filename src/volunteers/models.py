"""Volunteers Models"""
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from accounts.models import BaseProfile
from .management.commands.generate_username import generate_username


class VolunteerProfile(BaseProfile):
    """Volunteer User Info"""

    organization = models.CharField("Organization", max_length=200, blank=True, null=True)
    emergency_contact = models.CharField("Emergency Contact", max_length=200, blank=True, null=True)
    days_available = models.CharField("Days Available", max_length=200, blank=True, null=True)
    food_pantry = models.BooleanField("Food Pantry", default=False)
    interview = models.BooleanField("Interview", default=False)
    bi_lingual = models.BooleanField("Bi Lingual", default=False)
    fund_raising = models.BooleanField("Fund Raising", default=False)
    board_member = models.BooleanField("Board Member", default=False)
    sunshine_committee = models.BooleanField("Sunshine Committee", default=False)
    solicit_donations = models.BooleanField("Solicit Donations", default=False)
    record_keeping = models.BooleanField("Record Keeping", default=False)
    truck_or_van = models.BooleanField("Truck or Van", default=False)
    pick_up_food = models.BooleanField("Pick up Food", default=False)
    deliver_food = models.BooleanField("Deliver Food", default=False)

    def __str__(self):
        """Return the volunteers full name as the object name."""
        return self.user.get_username()


class VolunteerManager(models.Manager):
    """Volunteer model custom queryset."""

    def get_queryset(self):
        """Only return users with a volunteer profile."""
        return super(VolunteerManager, self).get_queryset().filter(
            groups__name__in=['Volunteers'])


class Volunteer(User):
    """Volunteer Model."""

    def __init__(self, *args, **kwargs):
        super(Volunteer, self).__init__(*args, **kwargs)

    objects = VolunteerManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        """Make sure created volunteers are added to the volunteers group and have a generated username"""
        volunteer_group, created = Group.objects.get_or_create(name='Volunteers')
        if not self.id:
            self.is_staff = False
            self.is_superuser = False
            self.username = generate_username(
                self.first_name,
                self.last_name
            )
            self.first_name = self.first_name.title()
            self.last_name = self.last_name.title()
        super(Volunteer, self).save()
        volunteer_group.user_set.add(self)


class TodaysSignedInVolunteersManager(models.Manager):
    """Manager for todays signed in volunteers."""

    def get_queryset(self):
        """Return only volunteer logs with todays date and a nonexistent sign_out_time."""
        todays_date = timezone.now().date()
        return super(TodaysSignedInVolunteersManager, self).get_queryset().filter(
            date=todays_date,
            sign_out_time__isnull=True
        )


class VolunteerLog(models.Model):
    """Volunteer logs with custom managers."""

    volunteer = models.ForeignKey(User)
    date = models.DateField()
    sign_in_time = models.DateTimeField()
    sign_out_time = models.DateTimeField(null=True, blank=True)
    total_volunteer_time = models.DurationField(null=True, blank=True)

    objects = models.Manager()
    logged_in_volunteers_objects = TodaysSignedInVolunteersManager()

    def __str__(self):
        """Return the volunteers full name as the object name."""
        return self.volunteer.get_username()

    def save(self, **kwargs):
        """If volunteer object doesn't have an ID (doesn't exist yet) save the creation time and date."""
        todays_date_time = timezone.now()
        todays_date = todays_date_time.date()
        if not self.id:
            self.sign_in_time = todays_date_time
            self.date = todays_date
        super(VolunteerLog, self).save()
