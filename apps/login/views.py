from django.shortcuts import render
from .forms import LoginForm
from . import manager

def index(request):
    form = manager.getForm(request)
    if manager.authenticate(request, form):
        return manager.redirect(request)
    return render(request, 'login/index.html', {'form': form})
