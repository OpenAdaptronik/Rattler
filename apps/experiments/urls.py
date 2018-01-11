from django.urls import path
from apps.experiments import views

app_name = 'experiments'
urlpatterns = [
    path('', views.index, name='index'),
]