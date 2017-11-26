from django.shortcuts import render

# Create your views here.
userdaten = {'username': None, 'email': None}
            username = request.POST['input-Nutzername']
            email = request.POST['input-Email']
            password = 'test'
            userdaten.update({'username': username, 'email': email})
            #user = User(userID=1, username= username, email= email, password=password)
            #user.save()
            user = User.objects.create_user(username, email, password)
            user.save()