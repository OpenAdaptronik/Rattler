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

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Login View
    path(
        'login/', 
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='/'),
        name='logout'
    ),

    # Password Views
    path(
        'password/',
        include('apps.password.urls'),
        name='password'
    ),
    #
    path('register/', include('apps.register.urls'), name='register'),
    # Django Admin
    path('admin/', admin.site.urls, name='admin'),
    # Global Routes
    path('dashboard/', views.dashboard, name='dashboard'),
    path('community/', include('apps.community.urls'), name='community'),
    path('profile/', include('apps.profile.urls'), name='profile'),
    path('createProjects/', include('apps.projects.urls'), name='createProjects'),
    path('help/', views.help, name='help'),
    path('process/', include('apps.process.urls'), name='process'),
    path('', include('apps.index.urls'), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
