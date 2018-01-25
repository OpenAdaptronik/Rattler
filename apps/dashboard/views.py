from django.shortcuts import render, HttpResponse
from apps.projects.models import Project
from django.contrib.auth.decorators import login_required

num_last_projects = 5

# Create your views here.
@login_required
def show_projects(request):
    last_projects = request.user.project_set.order_by('-experiment__created', '-updated', '-created')[:num_last_projects]
    return render(request, 'dashboard/index.html', {'last_projects': last_projects})
