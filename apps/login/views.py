from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .forms import LoginForm
from . import manager
from django.contrib.auth.decorators import login_required

def index(request):
    form = manager.getForm(request)
    if manager.authenticate(request, form):
        return HttpResponseRedirect('/login/home')
    return render(request, 'login/index.html', {'form': form})

@login_required
def home(request):
    return render(request, 'login/home.html', {'user':  request.user})

def logout(request):
    manager.logout(request)
    return HttpResponseRedirect('/login')