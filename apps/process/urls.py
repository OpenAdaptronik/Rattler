from django.urls import path

from apps.process import views

urlpatterns = [
    path('', views.index, name='index')
]