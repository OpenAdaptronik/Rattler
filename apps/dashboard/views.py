from django.shortcuts import render, HttpResponse
from apps.projects.models import Project
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def show_projects(request):
    user_id = request.user.id
    my_projects = Project.objects.filter(user_id=user_id).values_list('name', flat=True)
    return render(request, 'dashboard/index.html', {'my_projects': my_projects})
