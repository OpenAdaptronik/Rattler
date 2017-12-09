from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from apps.userSettings.forms import UserSettingsForm


def userSettings(request):
    respo = {'username': request.user.username, 'email': request.user.mail, 'company': request.user.company, 'infos': request.user.address}
    if request.method == 'POST':
        form = UserSettingsForm(data=request.POST, instance=request.user)
        if form.is_valid():
           user = form.save()
           user.save()
           return render(request, 'userSettings/index.html', respo) # hier neuladen, aber ich weiß den Befehl leider nicht
    return render(request, 'userSettings/index.html', respo)

