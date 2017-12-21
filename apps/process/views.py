from django.shortcuts import render

# Create your views here.
def fromDashboard(request):
    
    return render(request, "process/index.html")