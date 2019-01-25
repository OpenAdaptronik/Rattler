from django.urls import path

from apps.quiver import views

app_name = 'quiver'
urlpatterns = [
    path('<int:experimentId>/', views.index, name='index'),
]
