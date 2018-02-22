import logging
from django.shortcuts import render, HttpResponseRedirect
from .forms import RegisterForm
from .forms import AuthenticationForm

logger = logging.getLogger(__name__)

def index(request):
    logger.info('home')

    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard')

    return render(
        request,
        'index/index.html',
        {
            'login_form': AuthenticationForm(),
            'registration_form': RegisterForm()
        }
    )
