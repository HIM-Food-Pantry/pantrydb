from django.core.urlresolvers import reverse

from accounts.tests import SetupUserAccountTest
from .test_setup import SetUpVolunteerManagerAccount


class AuthAndPermissionVolunteerLogViewTests(SetupUserAccountTest):
    """Test volunteer log view denies users"""

    def test_volunteer_log_view_denies_anonymous(self):
        """Redirect Anonymous Users"""
        response = self.client.get(reverse('volunteers:sign-in-sheet'))
        self.assertRedirects(response, '/login/?next=/sign-in-sheet/')
        response = self.client.post(reverse('volunteers:sign-in-sheet'))
        self.assertRedirects(response, '/login/?next=/sign-in-sheet/')

    def test_user_doesnt_have_permission(self):
        """Test user created in Accounts App Test doesn't have permission"""
        self.client.login(
            username='test_user',
            password='top_secret'
        )
        response = self.client.get(reverse('volunteers:sign-in-sheet'))
        self.assertRedirects(response, '/login/?next=/sign-in-sheet/', status_code=302, target_status_code=302)


class VolunteerLogViewTests(SetUpVolunteerManagerAccount):
    def test_sign_in_log_volunteer_doesnt_exist(self):
        response = self.client.post(reverse('volunteers:sign-in-sheet'), {
            'sign_in-first_name': 'nonexistent',
            'sign_in-last_name': 'user',
            'sign_in-zip_code_name': '77000',

        })
        self.assertEqual(response.status_code, 200)

        self.assertFormError(
            response,
            'log_sign_in_form',
            field=None,
            errors=u"Volunteer does not exist, try again or click this <a href=\"/create-volunteer/\">Create Volunteer</a> link to create a volunteer profile")

    def test_sign_in_and_out_success(self):
        # Sign-in-sheet sign_in_volunteers is initially empty
        response = self.client.get(reverse('volunteers:sign-in-sheet'))
        self.assertContains(response, "No volunteers are currently signed in.")
        self.assertQuerysetEqual(response.context['signed_in_volunteers'], [])
        self.assertEqual(response.status_code, 200)

        # Post request sign-in-sheet view with LogSignInForm
        response = self.client.post(reverse('volunteers:sign-in-sheet'), {
            'sign_in-first_name': self.volunteer.first_name,
            'sign_in-last_name': self.volunteer.last_name,
            'sign_in-zip_code_name': self.volunteer_profile.zip_code
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('volunteers:sign-in-sheet'))
        # Redirected page contains list of signed in users
        self.assertQuerysetEqual(
            response.context['signed_in_volunteers'],
            ['<VolunteerLog: test_volunteer_useraccount>']
        )

        # Post LogSignOutForm
        response = self.client.post(reverse('volunteers:sign-in-sheet'), {
            'sign_out-first_name': self.volunteer.first_name,
            'sign_out-last_name': self.volunteer.last_name
        })
        self.assertRedirects(response, reverse('volunteers:sign-in-sheet'), status_code=302, target_status_code=200,
                             host=None, msg_prefix='',
                             fetch_redirect_response=True)
        # Response containers empty log list
        response = self.client.get(reverse('volunteers:sign-in-sheet'))
        self.assertQuerysetEqual(response.context['signed_in_volunteers'], [])


class CreateVolunteerViews(SetUpVolunteerManagerAccount):
    def test_create_volunteer_view(self):
        # Sign-in-sheet sign_in_volunteers is initially empty
        response = self.client.get(reverse('volunteers:create-volunteer'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('volunteers:create-volunteer'), {
            'first_name': 'create_new',
            'last_name': 'volunteer_user',
            'email': 'create_volunteer@test.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('volunteers:sign-in-sheet'))
