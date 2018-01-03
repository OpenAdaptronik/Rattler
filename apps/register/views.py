""" License
MIT License

Copyright (c) 2017 OpenAdaptronik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from django.shortcuts import HttpResponseRedirect, render

from django.template.loader import render_to_string

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.views.generic import FormView

from rattler.auth.mixins import NoLoginRequiredMixin
from rattler.auth.decorators import not_login_required

from .forms import RegisterForm
from .tokens import account_activation_token

class IndexView(NoLoginRequiredMixin, FormView):
    """Register Index View Class.

    Shows and handles the registration form.
    Extends rattler.auth.mixins.NoLoginRequiredMixin
    and django.views.generic.FormView.

    Attributes:
        See django.views.generic.FormView
        See rattler.auth.mixins.NoLoginRequiredMixin
    """
    template_name = 'register/index.html'
    form_class = RegisterForm
    success_url = 'success'

    def form_valid(self, form):
        """Called if the form is valid

        Saves the new generated user and sends an verification email

        Args:
            form: The registration form.

        Returns:
            Form valid redirection
        """

        user = form.save()
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
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
                    'uid': uid,
                    'token': token,
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

    Args:
        request: The called request

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

    Args:
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
