from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, RequestFactory

from volunteers.models import VolunteerProfile, VolunteerLog, Volunteer


class SetUpVolunteerUser(TestCase):
    def setUp(self):
        """Initialize the SetupUserAccountsTest and create a volunteer profile"""
        super(SetUpVolunteerUser, self).setUp()
        self.factory = RequestFactory()
        self.volunteer = Volunteer.objects.create(
            first_name='test_volunteer_user',
            last_name='account',
            email='test_volunteer@user.com',
            password='top_secret'
        )
        self.volunteer_profile = VolunteerProfile.objects.create(
            user=self.volunteer,
            zip_code='70000'
        )
        volunteer_group = Group.objects.get_or_create(name="Volunteers")
        volunteer_group[0].user_set.add(self.volunteer)


class SetUpVolunteerManagerAccount(SetUpVolunteerUser):
    def setUp(self):
        """Initialize the SetupUserAccountsTest and create a volunteer profile"""
        super(SetUpVolunteerManagerAccount, self).setUp()
        content_type = ContentType.objects.get_for_model(VolunteerLog)
        view_log_permission = Permission.objects.get(content_type=content_type, codename='add_volunteerlog')
        change_log_permission = Permission.objects.get(content_type=content_type, codename='change_volunteerlog')
        self.volunteer_manager = User.objects.create_user(
            first_name='volunteer_manager',
            last_name='user',
            username='volunteer_manager_user',
            password='super_password'
        )
        self.volunteer_manager.user_permissions.add(view_log_permission, change_log_permission)
        self.client.login(username=self.volunteer_manager.username,
                          password='super_password')
