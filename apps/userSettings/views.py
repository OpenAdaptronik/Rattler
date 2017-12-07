from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from apps.userSettings.forms import userSettingsForm


def userSettings(request):
   #current_user = request.user
   #print(current_user)
   if request.method == 'POST':

       form = userSettingsForm(data=request.POST, instance=request.user)

       if form.is_valid():
           user = form.save()
           user.save()
           return render(request, 'userSettings/index.html')
   return render(request, 'userSettings/index.html')

