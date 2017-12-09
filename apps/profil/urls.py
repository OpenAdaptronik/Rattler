from django.urls import path

from . import views

urlpatterns = [
    path('me', views.show_me()),#hier Name der Funktion in views
    # für anderen User  name =<slug:token>
    ]
