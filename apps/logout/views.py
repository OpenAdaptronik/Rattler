from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import logout

def index(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect('/')