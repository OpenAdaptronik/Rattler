from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

def index(request):
   
    if not request.user.is_authenticated:
        return render(
            request,
            'index/index.html',
            {
                'login_form': AuthenticationForm()
            }
        )
    else:
        return render(request, 'dashboard/index.html')
