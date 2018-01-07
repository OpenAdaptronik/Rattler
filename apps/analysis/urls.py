from django.urls import path

from apps.analysis import views

app_name = 'analysis'
urlpatterns = [
    path('', views.index, name='index'),
]