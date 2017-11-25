from django.shortcuts import render

def index (request):
    return render (request,'index.html')

def dashboard (request):
    return render (request,'dashboard/index.html')

def error404 (request):
    return render (request,'error404/index.html')

def register (request):
    return render (request,'register/index.html')

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

def logout (request):
    return render (request,'logout/index.html')

def help (request):
    return render (request,'help/index.html')
