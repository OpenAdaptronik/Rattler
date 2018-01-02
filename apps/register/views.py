"""
Views of the register app.
"""
from django.views.generic import FormView
from django.template.loader import render_to_string
from django.contrib import auth
from django.shortcuts import HttpResponseRedirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rattler.auth.mixins import NoLoginRequiredMixin
from rattler.auth.decorators import not_login_required

from apps.profile.models import Profile

from .forms import RegisterForm
from .models import VerificationToken
from .tokens import account_activation_token
from django.contrib.auth import get_user_model

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode



class IndexView(NoLoginRequiredMixin, FormView):
    """Register Index View Class

    Shows and handles the registrations url
    """
    template_name = 'register/index.html'
    form_class = RegisterForm
    success_url = 'success'

    def form_valid(self, form):
        """Called if the form is valid

        Saves the new generated user and sends an verification email

        Arguments:
            form {RegisterForm} -- The registration form.

        Returns:
            HttpResponseRedirect -- Form valid redirection
        """
        user = form.save()
        token = VerificationToken.objects.create_user_token(user)
        current_site = get_current_site(self.request)
        domain = current_site.domain
        user.email_user(
            'Account Verifikation',
            render_to_string(
                'register/mail/verification.html',
                {
                    'use_https': self.request.is_secure(),
                    'domain':domain,
                    'user': user,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                }
            )
        )
        return super().form_valid(form)


@not_login_required
def register_success(request):
    """The registration success view

    Renders the registration view

    Decorators:
        not_login_required

    Arguments:
        request {Request} -- The called request

    Returns:
        HttpResponse -- The rendered Response
    """
    return render(request, 'register/success.html')

@not_login_required
def register_activate(request, uidb64, token):
    """Verifies the user by the given token.

    Verifies the user and redirects to home

    Decorators:
        not_login_required

    Arguments:
        request {Request} -- The called request
        token {string} -- The verify token

    Returns:
        HttpResponse -- The redirection response
    """

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)

    return HttpResponseRedirect('/')
