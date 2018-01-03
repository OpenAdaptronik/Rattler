from django.shortcuts import render, HttpResponseRedirect

from .forms import AuthenticationForm
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard')

    return render(
        request,
        'index/index.html',
        {
            'login_form': AuthenticationForm()
        }
    )
