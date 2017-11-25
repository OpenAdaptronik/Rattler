from django.shortcuts import render

def index (request):
    return render (request,'index.html')

def dashboard (request):
    return render (request,'dashboard/index.html')

def error (request):
    return render (request,'error404/index.html')
