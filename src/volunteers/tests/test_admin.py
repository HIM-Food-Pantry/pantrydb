from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from accounts.tests import SetupUserAccountTest
from volunteers.models import Volunteer


class AdminVolunteerTest(SetupUserAccountTest):
    def test_add_volunteer_on_admin_site(self):
        """Creating volunteers should get_or_create the Volunteers group and automatically add the user to the volunteers group"""
        # Sanity check
        user = User.objects.get(username=self.user.username)
        self.assertEquals(user.username, self.user.username)
        # Give the user superuser privileges
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
        self.client.login(
            username=self.user.username,
            password='top_secret'
        )

        # Check that client can access the page
        response = self.client.get(reverse('admin:volunteers_volunteer_add'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('admin:volunteers_volunteer_add'), {
            'first_name': 'testvolunteer',
            'last_name': 'user',
            'volunteerprofile-0-zip_code': '70000',
            '_continue': 'Save and continue editing',
            'volunteerlog_set-INITIAL_FORMS': '0',
            'volunteerlog_set-TOTAL_FORMS': '3',
            'volunteerprofile-INITIAL_FORMS': '0',
            'volunteerprofile-TOTAL_FORMS': '1',
        })

        self.assertEqual(response.status_code, 302)
        # Name will return capitilized, check volunteer profile field as well
        volunteer = Volunteer.objects.get(first_name='Testvolunteer', last_name='User',
                                          volunteerprofile__zip_code='70000')
        request = self.client.get(reverse('admin:volunteers_volunteer_change', args={volunteer.id}))
        self.assertEqual(request.context['adminform'].form.initial['username'], volunteer.username)
