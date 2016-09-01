from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Volunteer, VolunteerLog, VolunteerProfile

User = get_user_model()


class VolunteerProfileInline(admin.StackedInline):
    """Inline volunteer profile used in VolunteerAdmin"""

    model = VolunteerProfile


class VolunteerLogInline(admin.StackedInline):
    """Inline volunteer logs used in VolunteerAdmin"""

    model = VolunteerLog


class VolunteerAdmin(admin.ModelAdmin):
    """Show only the volunteer fields"""

    inlines = [VolunteerProfileInline, VolunteerLogInline]

    def add_view(self, request, extra_content=None):
        """Username will be automatically created if not filled out"""
        self.fieldsets = (
            ('Personal Info', {
                'fields': (
                    'first_name',
                    'last_name',
                    'email'
                )}),
        )
        return super(VolunteerAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        """Username is still editable, I guess?"""
        self.fieldsets = (
            ('Personal Info', {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'username',
                )}),
        )
        return super(VolunteerAdmin, self).change_view(request, object_id)


# Register your models here.
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(VolunteerLog)
