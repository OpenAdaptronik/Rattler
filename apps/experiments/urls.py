from django.urls import path
from apps.experiments import views

app_name = 'experiments'
urlpatterns = [
    path('new/save', views.newESave, name='newESave'),
    path('new/<int:id>', views.newE, name='new'), # id is the id of the project the new experiment should be added to
    path('<int:experimentId>', views.index, name='index'),
    #path('<int:id>', views.index, name='index'),
]