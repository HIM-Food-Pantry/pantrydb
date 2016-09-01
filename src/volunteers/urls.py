"""Volunteers urls"""
from django.conf.urls import url

from .views import VolunteerSignInView, CreateVolunteerView

urlpatterns = [
    url(r'^sign-in-sheet/$', VolunteerSignInView.as_view(), name='sign-in-sheet'),
    url(r'^create-volunteer/$', CreateVolunteerView.as_view(), name='create-volunteer'),
]
