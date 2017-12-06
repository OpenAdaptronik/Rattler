from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
def userSettings(request):
   '''current_user = request.user
    print(current_user)'''
   return render(request, 'userSettings/index.html')