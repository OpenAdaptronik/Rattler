from django.urls import path
from . import views

app_name = 'community'
urlpatterns = [

    path('', views.user_filter, name='index')
    ]
