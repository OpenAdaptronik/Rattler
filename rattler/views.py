from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.templatetags.static import static 

@login_required
def dashboard(request):
    return render(request, 'dashboard/index.html')

def error404 (request):
    return render (request,'error404/index.html')

def about (request):
    return render (request,'about.html')

def license (request):
    return render (request,'license.html')

@login_required
def community (request):
    return render (request,'community/index.html')

@login_required
def profileMe (request):
    return render (request,'profileMe/index.html')

@login_required
def admin (request):
    return render (request,'admin/index.html')

@login_required
def settings (request):
    return render (request,'settings/index')

@login_required
def projects (request):
    return render (request, 'projects/create.html')

def help (request):
    return HttpResponseRedirect('/static/Benutzerhandbuch.pdf')

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


def sleep(request):
    import time
    time.sleep(4)
    return HttpResponseRedirect('/')

def fac(request, n):
    res = 1
    while n > 1:
        res = res * n
        n = n - 1
    return HttpResponse(res)