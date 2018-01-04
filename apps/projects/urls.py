from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.show_projects, name='showProjects'),
   # path('', views.save_project, name='index'),
    path('new/', views.NewProject.as_view(), name='new'),
    path('detail/<slug:name>/<int:id>', views.detail, name='detail'),
]
