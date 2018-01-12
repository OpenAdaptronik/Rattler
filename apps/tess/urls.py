from django.urls import path
from apps.tess import views

app_name = 'tess'
urlpatterns = [
    path('', views.index, name='index'),
    path('refresh', views.refresh_data, name='refresh'),
]