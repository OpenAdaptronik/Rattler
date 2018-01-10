from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.MyProjects.as_view(), name='index'),
    path('page/<int:page>', views.MyProjects.as_view(), name='index_paginated'),
    path('new/', views.NewProject.as_view(), name='new'),
    path('detail/<str:name>/<int:id>', views.detail, name='detail'),
    path('categories/', views.categories, name='categories'),
    path('categories/<int:id>/', views.categories, name='sub_categories'),
    #path('createExperiment/<slug:name>/<int:id>', views.createExperiment, name='createExperiment'),
]
