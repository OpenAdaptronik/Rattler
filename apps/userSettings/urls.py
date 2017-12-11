from django.test.signals import auth_password_validators_changed
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name='userSettings'
urlpatterns = [
    #url('changeEmail/', views.changeEmail, name='changeEmail'),
    path(
        'changePassword/',
         auth_views.PasswordChangeView.as_view(
            success_url='userSettings.index.html'
         ),
    name='changePassword'),
    path('', views.userSettings, name='index')
    ]