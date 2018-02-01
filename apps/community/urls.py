from django.urls import path
from apps.community import views
#from apps.profile import views

app_name = 'community'
urlpatterns = [
    path('', views.FilterListView.as_view(), name='index'),
    path('page-<int:page>/', views.FilterListView.as_view(), name='index_paginated')
]
