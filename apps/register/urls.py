"""URLs for the registration app"""
from django.urls import path
from .views import IndexView, register_success, register_activate 

app_name = 'register'
urlpatterns = [
    path('activate/<uidb64>/<slug:token>/', register_activate, name='activate'),
    path('success/', register_success, name='success'),
    path('', IndexView.as_view(), name='index'),
]
