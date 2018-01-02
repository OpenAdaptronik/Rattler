from django.urls import path
from . import views

app_name = 'profile'
urlpatterns = [
    path('', views.show_me, name='index'),
    path('edit/', views.ProfileUpdate.as_view(), name="edit"),
    path('edit/image/', views.ProfileImageUpdate.as_view(), name="edit_image"),
    path('<slug:name>/', views.show, name="profile"),
]
