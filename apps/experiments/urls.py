from django.urls import path
from apps.experiments import views

app_name = 'experiments'
urlpatterns = [
    path('new/save', views.newESave, name='newESave'),
    path('new/<int:id>', views.newE, name='new'), # id is the id of the project the new experiment should be added to
    # path("newexperiments/intderivate" , views.intderivate ,name='intderivate'),
    # path('newexperiments/refresh', views.refreshData ,name='refresh'),
    path('<int:experimentId>/derivate/refresh/', views.derivateRefresh ,name='derivateRefresh'),
    path('<int:experimentId>/derivate/', views.derivate, name='derivate'),
    path('<int:experimentId>/', views.index, name='index'),
    path('', views.index, name='index'),
]