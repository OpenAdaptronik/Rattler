from django.urls import path
from apps.experiments import views

app_name = 'experiments'
urlpatterns = [
    path('new/<int:id>', views.newE, name='new'),
    path('', views.index, name='index'),
    #path('<int:id>', views.index, name='index'),
]