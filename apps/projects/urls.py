from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.MyProjects.as_view(), name='index'),
    path('page/<int:page>', views.MyProjects.as_view(), name='index_paginated'),
    path('new/', views.NewProject.as_view(), name='new'),
    path('edit/<int:id>', views.UpdateProject.as_view(), name='edit'),
    path('detail/<str:name>/<int:id>', views.ProjectDetail.as_view(), name='detail'),
    path('categories/', views.categories, name='categories'),
    path('categories/<int:id>/', views.categories, name='sub_categories'),
    path('createExperiment/<slug:name>/<int:id>', views.createExperiment, name='createExperiment'),
]
