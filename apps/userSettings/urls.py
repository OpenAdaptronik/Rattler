
from django.urls import path

from . import views

app_name='userSettings'
urlpatterns = [
    path('userSettings', views.userSettings, name='userSettings')
    ]