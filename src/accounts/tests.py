from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory


class SetupUserAccountTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test_user',
            first_name='test',
            last_name='user',
            email='test@user.com',
            password='top_secret'
        )


class AccountsLogViewTests(SetupUserAccountTest):
    def test_logged_in_user_login_view_redirects_to_home(self):
        self.client.login(username='test_user',
                          password='top_secret')
        response = self.client.get(reverse('accounts:login'))
        self.assertRedirects(response, reverse('home'))

    def test_login_in_view_success(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'test_user',
            'password': 'top_secret',
            'remember_me': True
        })
        self.assertRedirects(response, reverse('home'))

    def test_sign_up_view_success(self):
        response = self.client.post(reverse('accounts:signup'), {
            'email': 'new@user.com',
            'password1': 'top_secret',
            'password2': 'top_secret',
            'username': 'newuser'
        })
        self.assertRedirects(response, reverse('home'))

    def test_password_change_view_success(self):
        self.client.login(username='test_user',
                          password='top_secret')
        response = self.client.post(reverse('accounts:password-change'), {
            'old_password': 'top_secret',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        })
        self.assertRedirects(response, reverse('home'))

    def test_password_reset_view_success(self):
        response = self.client.post(reverse('accounts:password-reset'), {
            'email': 'test@user.com',
        })
        self.assertRedirects(response, reverse('accounts:password-reset-done'))
        self.assertEqual(len(mail.outbox), 1)

        # Now, here's the kicker: we get the token and userid from the response

        token = response.context[0]['token']
        uid = response.context[0]['uid']
        # Now we can use the token to get the password change form
        # Now we post to the same url with our new password:
        response = self.client.post(reverse('accounts:password-reset-confirm',
                                            kwargs={'token': token, 'uidb64': uid}),
                                    {'new_password1': 'newpassword', 'new_password2': 'newpassword'})
        self.assertRedirects(response, reverse('home'))
