from django.urls import path

from apps.process import views

app_name = 'process'
urlpatterns = [
    path('', views.from_dashboard, name='from_dashboard'),
    path('analysis/', views.analysis, name='analysis'),
]