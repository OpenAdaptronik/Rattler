from apps.projects.models import Category, Project
from django.shortcuts import render, HttpResponse

from django.views.generic import FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProjectForm
from django.core import serializers


def save_project(request):
    # Submit project attributes
    if request.method == 'POST':
        post_data = request.POST.copy()
        category_name = post_data['category']
        subcategory_name = post_data['subcategory']
        projectname = post_data['projectname']
        manufacturer = post_data['manufacturer']
        typ = post_data['typ']
        description = post_data['description']
        visibility = post_data['visibility']

        try:
            category = Category.objects.get(name=category_name, parent=None)
        except Category.DoesNotExist:
            category = Category(name=category_name)
            category.save()

        try:
            subcategory = Category.objects.get(name=subcategory_name, parent=category)
        except Category.DoesNotExist:
            subcategory = Category(name=subcategory_name, parent=category)
            subcategory.save()

        project = Project(
            user=request.user,
            name=projectname,
            category=category,
            subcategory=subcategory,
            manufacturer=manufacturer,
            typ=type,
            description=description,
            visibility=visibility
        )

        project.save()

        return render(request, 'projects/create.html')

    return render(request, 'projects/create.html')

class NewProject(LoginRequiredMixin, CreateView):
    form_class=ProjectForm
    template_name = 'projects/project_create.html'

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.save()
        return super(NewProject, self).form_valid(form)

def categories(request, id=None):
    return render(
        request,
        'projects/categories.html',
        {
            'categories': Category.objects.filter(parent=id)
        }
    )


def detail(request, name, id):
    from django.shortcuts import HttpResponse
    return HttpResponse('%s %s' % (name, id))