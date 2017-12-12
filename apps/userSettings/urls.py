from django.urls import path
from . import views

app_name='settings'
urlpatterns = [
    path('changeEmail/', views.changeEmail, name='changeEmail'),
    path('changePassword/', views.changePassword, name='changePassword'),

    path('', views.userSettings, name='index')
    ]