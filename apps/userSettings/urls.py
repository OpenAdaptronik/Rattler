from django.urls import path
from . import views

app_name='settings'
urlpatterns = [
    path('changeEmail/', views.changeEmail, name='changeEmail'),
    path('changeEmail/<email>/<uidb64>/<token>/', views.changeEmailsucess, name='changeEmailSucess'),
    path('changePassword/', views.changePassword, name='changePassword'),

    path('', views.userSettings, name='index')
    ]