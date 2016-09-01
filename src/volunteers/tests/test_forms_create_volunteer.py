from django.core.urlresolvers import reverse

from volunteers.forms import CreateVolunteerProfileForm
from volunteers.models import Volunteer
from .test_setup import SetUpVolunteerManagerAccount


class CreateVolunteerFormTests(SetUpVolunteerManagerAccount):
    def test_create_volunteer_form(self):
        form_data = {
            'first_name': 'create_volunteer_form',
            'last_name': 'user',
            'email': 'create_volunteer_form@gmail.com',
            'zip_code': '77000'
        }
        form = CreateVolunteerProfileForm(data=form_data)
        form.is_valid()
        self.assertTrue(form.is_valid())
        form.save()
        volunteer = Volunteer.objects.get(
            username='create_volunteer_formuser',
            volunteerprofile__zip_code=form_data['zip_code']
        )

        # Names are returned capitilized
        self.assertEquals(volunteer.username, "create_volunteer_formuser")
        self.assertEquals(volunteer.first_name, "Create_Volunteer_Form")
        self.assertEquals(volunteer.last_name, "User")

    def test_create_volunteer_form_user_exists(self):
        request = self.factory.get(reverse('volunteers:create-volunteer'))
        request.user = self.volunteer_manager
        form_data = {
            'first_name': self.volunteer.first_name,
            'last_name': self.volunteer.last_name,
            'email': self.volunteer.email,
            'zip_code': self.volunteer.volunteerprofile.zip_code
        }
        form = CreateVolunteerProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
