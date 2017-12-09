from django.shortcuts import render

# Create your views here.

def show_me(request):
    respo = {'username': request.user.username, 'email': request.user.mail, 'company': request.user.company,
             'infos': request.user.address}

    return render(request, 'profile/index.html', respo)

#def show_user(request, name):
#    return