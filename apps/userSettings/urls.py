from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.userSettings, name='index'),
]
'''from django.urls import path

from . import views

app_name='userSettings'
urlpatterns = [
    path('userSettings', views.userSettings, name='userSettings')
    ]'''