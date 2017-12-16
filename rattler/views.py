from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
import pprint

@login_required
def dashboard (request):
    return render (request,'dashboard/index.html')

def error404 (request):
    return render (request,'error404/index.html')

def registerTest (request):
    return render (request,'register/test/test.html')

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
def help (request):
    return render (request,'help/index.html')

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index/index.html')
    else:
        return render(request, 'dashboard/index.html')

def header(request):
    pp = pprint.PrettyPrinter(indent=4)
    return HttpResponse(pp.pformat(request.META), content_type="text/plain")

