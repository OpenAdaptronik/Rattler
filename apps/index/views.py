from django.shortcuts import render

from .forms import AuthenticationForm
def index(request):
    return render(
        request, 
        'index/index.html', 
        {
            'login_form': AuthenticationForm()
        }
    )
