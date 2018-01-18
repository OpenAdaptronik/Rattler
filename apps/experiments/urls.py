from django.urls import path
from apps.experiments import views

app_name = 'experiments'
urlpatterns = [
    path('', views.index, name='index'),
    path('new/<int:id>', views.newE, name='new'),
    path("newexperiments/intderivate" , views.intderivate ,name='intderivate'),
    path('newexperiments/refresh', views.refreshData ,name='refresh'),
]