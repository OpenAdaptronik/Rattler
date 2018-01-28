from django.shortcuts import render
from apps.user.models import User
from apps.profile.models import Profile
from django.contrib.auth.decorators import login_required
from apps.projects.models import Project
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import QueryDict

'''Community'''
class FilterListView(ListView):
    model = Project
    template_name = 'community/index.html'
    context_object_name = "filtered"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        data = super(FilterListView, self).get_context_data(**kwargs)
        data['filter'] = {}

        username = self.request.GET.get('username', False)

        if username:
            data['filter']['username'] = username

        company = self.request.GET.get('company', False)
        if company:
            data['filter']['company'] = company

        email = self.request.GET.get('email', False)
        if email:
            data['filter']['email'] = email

        projectname = self.request.GET.get('projectname', False)
        if projectname:
            data['filter']['projectname'] = projectname

        category = self.request.GET.get('category', False)
        if category:
            data['filter']['category'] = category

        manufacturer = self.request.GET.get('manufacturer', False)
        if manufacturer:
            data['filter']['manufacturer'] = manufacturer

        qdict = QueryDict('', mutable=True)
        qdict.update(data['filter'])
        data['filter_url'] = qdict.urlencode()
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
