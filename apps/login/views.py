from django.shortcuts import render
from . import insertNewUser
from .models import User
from django.contrib.auth.models import User




def login(request):
    if request.method == 'POST':
        if request.POST["art"]=="register":
            userdaten = {'username': None, 'email': None}
            username = request.POST['input-Nutzername']
            email = request.POST['input-Email']
            password = 'test'
            userdaten.update({'username': username, 'email': email})
            #user = User(userID=1, username= username, email= email, password=password)
            #user.save()
            user = User.objects.create_user(username, email, password)
            user.save()
            #insertNewUser.enter_data(username, email, password)
            return render(request, 'login/index.html', userdaten)
        else:
            logindaten = {'loginname': None, 'loginpassword': None}
            loginname = request.POST['input-login-name']
            loginpassword = request.POST['input-login-password']
            logindaten.update({'loginname': loginname, 'loginpassword': loginpassword})
            # hier Funktion, die eingegebene Daten überprüft
            return render(request, 'login/index.html', logindaten)

    return render(request, 'login/index.html')