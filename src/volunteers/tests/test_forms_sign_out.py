from volunteers.forms import LogSignOutForm
from .test_setup import SetUpVolunteerManagerAccount


class VolunteerLogFormTests(SetUpVolunteerManagerAccount):
    def test_sign_out_form(self):
        form_data = {
            'sign_out-first_name': 'test',
            'sign_out-last_name': 'user'
        }
        form = LogSignOutForm(data=form_data)
        self.assertTrue(form.is_valid())
