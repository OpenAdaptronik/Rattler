from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from apps.userSettings.forms import userSettingsForm


def userSettings(request):
    respo = {'username': request.user.username, 'email': request.user.mail, 'firma': request.user.firma, 'infos': request.user.adresse}
    if request.method == 'POST':
        form = userSettingsForm(data=request.POST, instance=request.user)
        if form.is_valid():
           user = form.save()
           user.save()
           return render(request, 'userSettings/index.html', respo) # hier neuladen, aber ich weiß den Befehl leider nicht
    return render(request, 'userSettings/index.html', respo)

