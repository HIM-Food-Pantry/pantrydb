"""Volunteer views"""
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import LogSignInForm, LogSignOutForm, CreateVolunteerProfileForm
from .models import VolunteerLog


class VolunteerSignInView(PermissionRequiredMixin, FormView):
    """Logs users in and out of the sign in sheet"""

    login_url = '/login/'
    template_name = "sign_in_page/base.html"
    success_url = reverse_lazy('volunteers:sign-in-sheet')
    permission_required = ['volunteers.add_volunteerlog', 'volunteers.change_volunteerlog']

    def get(self, request):
        """Get the sign in sheet view with the LogSignInForm and list of currently signed in volunteers"""
        context = {
            'signed_in_volunteers': VolunteerLog.logged_in_volunteers_objects.all(),
            'log_sign_in_form': LogSignInForm
        }
        return render(self.request, self.template_name, context)

    def post(self, request):
        """Sign in and out forms each have a prefix. Checks which form is posted"""
        context = {
            'signed_in_volunteers': VolunteerLog.logged_in_volunteers_objects.all(),
            'log_sign_in_form': LogSignInForm
        }
        if request.method == 'POST':
            log_sign_out_form = LogSignOutForm(request.POST)
            if log_sign_out_form.is_valid():
                log_sign_out_form.save()
                return super(VolunteerSignInView, self).form_valid(log_sign_out_form)

        if request.method == 'POST' and not log_sign_out_form.is_valid():
            log_sign_in_form = LogSignInForm(request.POST)
            if log_sign_in_form.is_valid():
                log_sign_in_form.save()
                return render(request, self.template_name, context)
            else:
                messages.error(request, "Please correct the errors below and resubmit.")
                context['log_sign_in_form'] = log_sign_in_form
                return render(request, self.template_name, context)


class CreateVolunteerView(FormView):
    """Form for creating a volunteer"""

    template_name = "create_volunteer.html"
    form_class = CreateVolunteerProfileForm
    login_url = '/login/'
    success_url = reverse_lazy('volunteers:sign-in-sheet')
    permission_required = ['volunteers.add_volunteerlog', 'volunteers.change_volunteerlog']

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return super(CreateVolunteerView, self).form_valid(form)
