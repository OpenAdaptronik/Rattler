from django.shortcuts import render
from apps.user.models import User
from apps.projects.models import Project

# Create your views here.

def filter(request):
    if request.method == 'POST':
        updated_data = request.POST.copy()
        searched_username = updated_data['username']
        #mehrere Werte -> Schleife
        projectId = User.objects.filter(username = searched_username).values()
        # Schleife
        wellenId = Project.objects.filter(projectID = projectId).values()



