from django.contrib import auth
from django.shortcuts import HttpResponseRedirect
from .forms import LoginForm

def isPost(request):
    return request.method == 'POST'

def getForm(request):
    if isPost(request):
        return LoginForm(request.POST)
    return LoginForm()

def authenticate(request, form):
    # Kein Post => Keine Daten zum Login
    if not isPost(request):
        return False
    # Formular gültig?
    if not form.is_valid(): 
        return False
    # User aus der Datenbank holen
    user = auth.authenticate(
        username=form.cleaned_data['name'],
        password=form.cleaned_data['password']
    )
    # Kein User gefunden
    if user is None:
        # Form Error hinzufügen!
        return False
    # User in Session eintragen
    auth.login(request, user)
    return True

def redirect(request):
    return HttpResponseRedirect(request.GET.get('next', '/'))

