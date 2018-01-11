from apps.projects.models import Category, Project
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from django.views.generic import FormView, CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProjectForm
from django.core import serializers
from django.utils.encoding import uri_to_iri

from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

class NewProject(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = 'projects/project_create.html'

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.save()
        return super(NewProject, self).form_valid(form)

class UpdateProject(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.user == self.request.user and not self.object.visibility:
            raise PermissionDenied()
        return super(UpdateProject, self).get(request, *args, **kwargs)

class MyProjects(LoginRequiredMixin, ListView):
    model = Project
    allow_empty = True
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(user=user).order_by('created')

class ProjectDetail(DetailView):
    model = Project
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.user == self.request.user and not self.object.visibility:
            raise PermissionDenied()
        return super(ProjectDetail, self).get(request, *args, **kwargs)


def categories(request, id=None):
    return render(
        request,
        'projects/categories.html',
        {
            'categories': Category.objects.filter(parent=id)
        }
    )

def createExperiment(request, name, id):
    if request.method == 'POST':
        post_data = request.POST.copy()
        description = post_data['description']
 
        new_experiment = Experiment(project_id=id, description=description)
        new_experiment.save()

    return render(request, 'projects/createExperiment.html')