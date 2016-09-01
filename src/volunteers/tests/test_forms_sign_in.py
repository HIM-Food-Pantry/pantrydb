from volunteers.forms import LogSignInForm
from .test_setup import SetUpVolunteerManagerAccount


class FailedSignInFormTests(SetUpVolunteerManagerAccount):
    def test_volunteer_doesnt_exist_by_email(self):
        form_data = {
            'sign_in-email': 'nonexistent@example.com',
        }
        form = LogSignInForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_volunteer_doesnt_exist_by_username_zip(self):
        form_data = {
            'sign_in-username': 'nonexistentuser',
            'sign_in-zip_code_username': '70000',
        }
        form = LogSignInForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_volunteer_doesnt_exist_by_name_zip(self):
        form_data = {
            'sign_in-first_name': 'nonexistent',
            'sign_in-last_name': 'user',
            'sign_in-zip_code_name': '70000',
        }
        form = LogSignInForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_empty_volunteer_form(self):
        form_data = {
            'sign_in-first_name': '',
            'sign_in-last_name': '',
            'sign_in-zip_code_name': '',
            'sign_in-zip_code_username': '',
            'sign_in-username': '',
        }
        form = LogSignInForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(u'Please fill out one of the following log in options.', form.errors['__all__'])


class SignInFormTests(SetUpVolunteerManagerAccount):
    def test_voluteer_sign_in_by_email(self):
        form_data = {
            'sign_in-email': self.volunteer.email,
        }
        form = LogSignInForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_voluteer_sign_in_by_username_zip(self):
        form_data = {
            'sign_in-username': self.volunteer.username,
            'sign_in-zip_code_username': self.volunteer_profile.zip_code,
        }
        form = LogSignInForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_volunteer_sign_in_by_name_zip(self):
        form_data = {
            'sign_in-first_name': self.volunteer.first_name,
            'sign_in-last_name': self.volunteer.last_name,
            'sign_in-zip_code_name': self.volunteer_profile.zip_code,
        }
        form = LogSignInForm(data=form_data)
        self.assertTrue(form.is_valid())
