from django.conf.urls import url

from . import views

app_name='userSettings'
urlpatterns = [
    #url('changeEmail/', views.changeEmail, name='changeEmail'),
    #url(r'^changePassword/', views.ChangePassword, name='changePassword'),
    url(r'^$', views.userSettings, name='userSettings')
    #path('userSettings', views.userSettings, name='userSettings')
    ]