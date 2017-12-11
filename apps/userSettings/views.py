from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from apps.userSettings.forms import UserSettingsForm


def userSettings(request):
   # respo = {'username': request.user.username, 'email': request.user.mail, 'company': request.user.company, 'infos': request.user.info}
    if request.method == 'POST':
        form = UserSettingsForm(data=request.POST, instance=request.user)
        user = form.save()
        return render(request, 'userSettings/index.html')
    return render(request, 'userSettings/index.html')

def ChangePassword(request):

    return render(request, 'userSettings/ChangePassword.html')
