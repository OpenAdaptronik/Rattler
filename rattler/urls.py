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
from django.conf.urls import include, url, handler404
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Import Apps
    url(
        'login/',
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name='login'
    ),
    url(
        'logout/',
        auth_views.LogoutView.as_view(next_page='/'),
        name='logout'
    ),
    url('register/', include('apps.register.urls'), name='register'),
    # Django Admin
    url('djangoAdmin/', admin.site.urls),
    # Global Routes
    url('dashboard/', views.dashboard, name='dashboard'),
    url('community/', views.community, name='community'),
    url('profile/me/', views.profileMe, name='profileMe'),
    url('admin/', views.admin, name='admin'),
    url('settings/', views.settings, name='settings'),
    url('help/', views.help, name='help'),



    url('', include('django.contrib.auth.urls')),


    url('', views.index, name='index'),
]

# Error Handlers
handler404 = 'rattler.views.handler404'