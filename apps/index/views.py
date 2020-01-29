import logging
from django.shortcuts import render, HttpResponseRedirect
from .forms import RegisterForm
from .forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)

@csrf_exempt
def index(request):
    logger.info('home')

    if request.method == 'POST':
        if request.POST.get("url") == 'testurl':
            # curl --data "post1=value1&post2=value2&etc=valetc&url=testurl" http://localhost
            # hier weiter arbeiten!!
            raise ValueError('bruh')
            return

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
