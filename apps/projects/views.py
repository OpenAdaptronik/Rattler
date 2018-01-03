from apps.projects.models import Category, Project
from django.shortcuts import render

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