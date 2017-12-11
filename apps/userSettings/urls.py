from django.urls import path
from django.contrib.auth.views import password_change
from . import views

app_name='userSettings'
urlpatterns = [
    #url('changeEmail/', views.changeEmail, name='changeEmail'),
    path('changePassword/', password_change, name='changePassword'),
    path('', views.userSettings, name='index')
    ]