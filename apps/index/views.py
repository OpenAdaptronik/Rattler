from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

def index(request):
    return render(
        request, 
        'index/index.html', 
        {
            'login_form': AuthenticationForm()
        }
    )
