"""Volunteer Forms"""
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe

from .models import VolunteerLog, Volunteer, VolunteerProfile


def check_volunteer_handle(cleaned_date):
    first_name = cleaned_date.get("first_name")
    last_name = cleaned_date.get("last_name")
    username = cleaned_date.get("username")
    email = cleaned_date.get("email")
    zip_code_username = cleaned_date.get("zip_code_username")
    zip_code_name = cleaned_date.get("zip_code_name")

    missing_fields_error = forms.ValidationError(
        mark_safe(
            (
                'Volunteer does not exist, try again or click this <a href="{0}">Create Volunteer</a> link to create a volunteer profile').format(
                reverse('volunteers:create-volunteer')))
    )

    if email:
        try:
            volunteer = Volunteer.objects.get(
                email=email
            )
        except Volunteer.DoesNotExist:
            raise missing_fields_error
        return volunteer

    if username and zip_code_username:
        try:
            volunteer = Volunteer.objects.get(
                username=username,
                volunteerprofile__zip_code=zip_code_username
            )
        except Volunteer.DoesNotExist:
            raise missing_fields_error
        return volunteer

    if first_name and last_name and zip_code_name:
        try:
            volunteer = Volunteer.objects.get(
                first_name=first_name,
                last_name=last_name,
                volunteerprofile__zip_code=zip_code_name
            )
        except Volunteer.DoesNotExist:
            raise missing_fields_error
        return volunteer

    if not email or username and zip_code_username or first_name and last_name and zip_code_name:
        raise forms.ValidationError("Please fill out one of the following log in options.")


class LogSignInForm(forms.Form):
    """Volunteer log sign in form"""

    first_name = forms.CharField(
        label='First Name',
        max_length=100,
        error_messages={'required': 'Please provide a first name'},
        required=False
    )

    last_name = forms.CharField(
        label='Last Name',
        max_length=100,
        error_messages={'required': 'Please provide a last name'},
        required=False
    )

    zip_code_name = forms.CharField(label='Zip Code', max_length=100, required=False)
    username = forms.CharField(label='Username', max_length=100, required=False)
    zip_code_username = forms.CharField(label='Zip Code', max_length=100, required=False)
    email = forms.EmailField(label='Email', max_length=100, required=False)

    prefix = 'sign_in'

    def clean(self):
        """Makes sure form has first_name and last_name and a volunteer exists, otherwise raise form error."""
        cleaned_data = super(LogSignInForm, self).clean()
        volunteer = check_volunteer_handle(cleaned_data)
        cleaned_data['volunteer'] = volunteer
        return self.cleaned_data

    def save(self, commit=True):
        """Take the cleaned data, create and save the new volunteer log"""
        data = self.cleaned_data
        volunteer = data['volunteer']
        if volunteer:
            volunteer_log = VolunteerLog(volunteer=volunteer)
            if commit:
                volunteer_log.save()
            return volunteer_log


class LogSignOutForm(forms.Form):
    """Sign the user out"""

    first_name = forms.CharField(
        label='First Name',
        max_length=100,
    )

    last_name = forms.CharField(
        label='Last Name',
        max_length=100,
    )

    prefix = 'sign_out'

    def save(self, commit=True):
        """Find volunteer and log, then get the time delta from sign in and out time."""
        data = self.cleaned_data
        now = timezone.now()
        volunteer = Volunteer.objects.get(
            first_name=data['first_name'],
            last_name=data['last_name'],
        )

        volunteer_log = VolunteerLog.logged_in_volunteers_objects.get(
            volunteer=volunteer,
        )
        volunteer_log.sign_out_time = now
        date_time_start = volunteer_log.sign_in_time
        date_time_stop = volunteer_log.sign_out_time
        date_time_delta = date_time_stop - date_time_start

        volunteer_log.total_volunteer_time = date_time_delta

        if commit:
            volunteer_log.save()
        return volunteer


class CreateVolunteerProfileForm(forms.Form):
    """This form is used when the volunteer log fails to find an existing volunteer"""

    email = forms.EmailField(required=False)
    zip_code = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(CreateVolunteerProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            ))

    def clean(self):
        cleaned_data = super(CreateVolunteerProfileForm, self).clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        email = cleaned_data.get('email')
        zip_code = cleaned_data.get('zip_code')

        try:
            volunteer = Volunteer.objects.get(
                email=email,
                last_name=last_name,
                first_name=first_name,
                volunteerprofile__zip_code=zip_code

            )
            if volunteer:
                raise forms.ValidationError("Please fill out one of the following log in options.")
        except Volunteer.DoesNotExist:
            volunteer = Volunteer(
                email=email,
                first_name=first_name,
                last_name=last_name
            )

            cleaned_data['volunteer'] = volunteer
            return self.cleaned_data

    def save(self, commit=True):
        data = self.cleaned_data
        volunteer = data['volunteer']

        if commit:
            volunteer.save()
            volunteer_profile = VolunteerProfile(
                user=volunteer,
                zip_code=data['zip_code']
            )
            volunteer_profile.save()
        return volunteer
