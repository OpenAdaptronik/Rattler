"""rattler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    # Import Apps
    url(r'^login/', include('apps.login.urls', namespace='login')),
    url(r'^logout/', include('apps.logout.urls', namespace='logout')),
    # Django Admin
    url(r'^admin/', admin.site.urls),
    # Global Routes
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^register/test/', views.registerTest, name='registerTest'),
    url(r'^register/', views.register, name='register'),
    url(r'^community/', views.community, name='community'),
    url(r'^profile/me/', views.profileMe, name='profileMe'),
    url(r'^settings/', views.settings, name='settings'),
    url(r'^help/', views.help, name='help'),
    url(r'^', include('apps.index.urls')),
    url(r'^', views.index),
]
