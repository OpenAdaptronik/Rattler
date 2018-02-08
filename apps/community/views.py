from django.shortcuts import render
from apps.user.models import User
from apps.profile.models import Profile
from django.contrib.auth.decorators import login_required
from apps.projects.models import Project
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

'''Community'''


class FilterListView(ListView):
    model = Project
    template_name = 'community/index.html'
    context_object_name = "filtered"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        data = super(FilterListView, self).get_context_data(**kwargs)
        data['filter'] = {
            'username': self.request.GET.get('username', None),
            'company': self.request.GET.get('company', None),
            'email': self.request.GET.get('mail', None),
            'projectname': self.request.GET.get('projectname', None),
            'category': self.request.GET.get('category', None),
            'manufacturer': self.request.GET.get('manufacturer', None),
        }
        return data

    def get_queryset(self):
        queryset = Project.objects.filter(visibility=True)
        username = self.request.GET.get('username', False)
        company = self.request.GET.get('company', False)
        email = self.request.GET.get('mail', False)
        projectname = self.request.GET.get('projectname', False)
        category = self.request.GET.get('category', False)
        manufacturer = self.request.GET.get('manufacturer', False)
        if username:
            queryset = queryset.filter(user__username__icontains=username)
        if email:
            queryset = queryset.filter(user__email__icontains=email)
        if company:
            queryset = queryset.filter(user__profile__company__icontains=company)
        if projectname:
            queryset = queryset.filter(name__icontains=projectname)
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        if manufacturer:
            queryset = queryset.filter(manufacturer__icontains=manufacturer)
        return queryset


def user_filter(request):
    filtered_ids = list(Project.objects.values_list('id', flat=True))
    filtered_ids = list(Project.objects.all().values_list('id', flat=True))
    # Submit User Search
    if request.method == 'POST':
        post_data = request.POST.copy()
        username = post_data['username']
        company = post_data['company']
        email = post_data['mail']
        project_name = post_data['projectname']
        category = post_data['category']
        manufacturer = post_data['manufacturer']
        # empty search

        if (username == '') and (email == '') and (company == '') and (project_name == '') and (category == '') \
                and (manufacturer == ''):
            return render(request, 'community/index.html', {'empty_search': 'Bitte gib einen Suchbegriff ein!'})

        # legitimate search
        if not(username == ''):
            matching_ids = list(Project.objects.filter(user__username__icontains=username).values_list('id', flat=True))
            filtered_ids = list(set(matching_ids) & set(filtered_ids))
        if not(email == ''):
            matching_ids = list(Project.objects.filter(user__email__icontains=email).values_list('id', flat=True))
            filtered_ids = list(set(matching_ids) & set(filtered_ids))
        if not(company == ''):
            matching_ids = list(Project.objects.filter(user__profile__company__icontains=company).
                                values_list('id', flat=True))
            filtered_ids = list(set(matching_ids) & set(filtered_ids))
        if not(project_name == ''):
            matching_ids = list(Project.objects.filter(name__icontains=project_name).values_list('id', flat=True))
            filtered_ids = list(set(matching_ids) & set(filtered_ids))
        if not(category == ''):
            matching_ids = list(Project.objects.filter(category__name__icontains=category).values_list('id', flat=True))
            filtered_ids = list(set(matching_ids) & set(filtered_ids))
        if not(manufacturer == ''):
            matching_ids = list(Project.objects.filter(manufacturer__icontains=manufacturer).
                                values_list('id', flat=True))
            filtered_ids = list(set(matching_ids) & set(filtered_ids))

    # no id matches
        if len(filtered_ids) == 0:
            return render(request, 'community/index.html', {'no_match': 'No user matches with your search, try again!'})

    filtered = filter(filtered_ids)
    return render(request, 'community/index.html', {'filtered': filtered})


def filter(filtered_ids):
    # return users and projects in filtered
    i = 0
    filtered_projects = list()
    while i < len(filtered_ids):
        currid = filtered_ids[i]
        filtered_projects.append(Project.objects.get(id=currid))
        i += 1

    j = 0
    filtered_users = list()
    while j < len(filtered_ids):
        currprojectid = filtered_ids[j]
        curruserid = Project.objects.get(id=currprojectid).user_id
        filtered_users.append(User.objects.get(id=curruserid))
        j += 1

    filtered = zip(filtered_users, filtered_projects)

    return filtered
