from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
def userSettings(request):
    return render(request, 'userSettings/index.html')