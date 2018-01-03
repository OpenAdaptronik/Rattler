'''
Views of the register app.
'''
from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth import get_user_model

from apps.projects.models import Project


def save_project(request):
    # Submit project attributes
    if request.method == 'POST':
        curruser = request.POST.user
        post_data = request.POST.copy()
        category = post_data['category']
        subcategory = post_data['subcategory']
        projectname = post_data['projectname']
        manufacturer = post_data['manufacturer']
        typ = post_data['typ']
        description = post_data['description']
        visibility = post_data['visibility']

        new_project = Project(user=curruser, category=category, subcategory=subcategory, projectname=projectname,
                              manufacturer=manufacturer, typ=typ, description=description, visibility=visibility)
        new_project.save()

        return render(request, 'projects/index.html')

    return render(request, 'projects/index.html')