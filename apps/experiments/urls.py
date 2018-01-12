from django.urls import path
from apps.experiments import views

app_name = 'experiments'
urlpatterns = [
    path('new/', views.newE, name='new'),
    path('', views.index, name='index'),
]