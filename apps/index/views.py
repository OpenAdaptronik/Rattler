import logging
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from .forms import RegisterForm
from .forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
import json


logger = logging.getLogger(__name__)

@csrf_exempt
def index(request):
    logger.info('home')

    if request.method == 'POST':
        data = json.loads(request.body.decode())
        if "url" in data and data["url"] == 'testurl':
            # curl --data "post1=value1&post2=value2&etc=valetc&url=testurl" https://rattler.openadaptronik.de
            # hier weiter arbeiten!!
            return HttpResponse(str(data) + "200")
        else:
            #return HttpResponse(str(type(request.body)) + "400", status=400) ["url"]
            return HttpResponse(str(data) + "400")

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
