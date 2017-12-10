from django.urls import path

from . import views

app_name='userSettings'
urlpatterns = [
    path('', views.userSettings, name='userSettings')
    ]