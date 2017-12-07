'''
Views of the register app.
'''
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import FormView, View
from django.template.loader import render_to_string
from django.contrib import auth
from django.shortcuts import HttpResponseRedirect

from .forms import RegisterForm
from .models import VerificationToken

class IndexView(FormView):
    template_name = 'register/index.html'
    form_class = RegisterForm
    success_url = '/register'
    def form_valid(self, form):
        user = form.save()
        token = VerificationToken.objects.create_user_token(user)
        user.email_user(
            'Test',
            render_to_string(
                'register/mail/verification.html',
                {
                    'user': user,
                    'token': token,
                }
            )
        )
        return super().form_valid(form)

class ActivateView(View):
    def get(self, request, token):
        token = VerificationToken.objects.get(token=token)
        if token == None:
            return HttpResponseRedirect('index:index')
        token.user.is_active = True
        token.user.save()
        auth.login(request, token.user)
        return HttpResponseRedirect('/')