from django.shortcuts import render
from apps.login.forms import LoginForm
from django.contrib.auth.decorators import login_required

def index (request):
    if not request.user.is_authenticated:
        return render (request,'index/index.html', {'form': LoginForm()})
    else:
        return dashboard(request)

@login_required
def dashboard (request):
    return render (request,'dashboard/index.html')

def error404 (request):
    return render (request,'error404/index.html')

def registerTest (request):
    return render (request,'register/test/test.html')

def community (request):
    return render (request,'community/index.html')

def profileMe (request):
    return render (request,'profileMe/index.html')

def admin (request):
    return render (request,'admin/index.html')

def settings (request):
    return render (request,'settings/index.html')

def help (request):
    return render (request,'help/index.html')

def handler404(request):
    return render(request, '404.html', status=404)