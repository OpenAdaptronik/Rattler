from apps.projects.models import Category, Project
from django.shortcuts import render

from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

def show_projects(request):
    user_id = request.user.id
    my_projects = Project.objects.filter(user_id=user_id) #.values_list('name', flat=True)
    return render(request, 'projects/showProjects.html', {'my_projects': my_projects})

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
    model=Project
    fields=('name', 'category', 'subcategory', )

    template_name_suffix = '_create'
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super(NewProject, self).form_valid(form)


def detail(request, name, id):
    from django.shortcuts import HttpResponse
    return HttpResponse('%s %s' % (name, id))