from django.shortcuts import render
from .forms import LoginForm
from . import manager
from django.contrib.auth.decorators import login_required

def index(request):
    form = manager.getForm(request)
    if manager.authenticate(request, form):
        return manager.redirect(request)
        return HttpResponseRedirect('/login/home')
    return render(request, 'login/index.html', {'form': form})

@login_required
def home(request):
    return render(request, 'login/home.html', {'user':  request.user})
