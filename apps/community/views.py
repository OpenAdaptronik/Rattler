from django.shortcuts import render
from apps.user.models import User
from apps.profile.models import Profile
from django.contrib.auth.decorators import login_required
from apps.projects.models import Project
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import QueryDict
from django.db.models import Q

'''Community'''


class FilterListView(ListView):
    model = Project
    template_name = 'community/index.html'
    context_object_name = "filtered"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        data = super(FilterListView, self).get_context_data(**kwargs)
        data['filter'] = {}

        search = self.request.GET.get('search', False)
        if search:
            data['filter']['search'] = search

        qdict = QueryDict('', mutable=True)
        qdict.update(data['filter'])
        data['filter_url'] = qdict.urlencode()
        return data

    def get_queryset(self):
        queryset = Project.objects.filter(visibility=True)
        search = self.request.GET.get('search', False)
        if search:
            queryset = queryset.filter(
                Q(user__username__icontains=search) | Q(user__email__icontains=search) |
                Q(user__profile__company__icontains=search) | Q(name__icontains=search) |
                Q(category__name__icontains=search) | Q(manufacturer__icontains=search) |
                Q(typ__icontains=search) | Q(subcategory__name=search)
            )

        return queryset
