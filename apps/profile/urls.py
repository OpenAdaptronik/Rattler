from django.urls import path
from . import views

app_name = 'profile'
urlpatterns = [
    path('', views.show_me, name='index'),
    path('edit/', views.ProfileUpdate.as_view(), name="edit"),
    path('edit/image/', views.ProfileImageUpdate.as_view(), name="edit_image"),
    path('<slug:name>/', views.show, name="detail"),
    path('change/email/', views.change_email, name='change_email'),
    path('change/email/success/<mail>/<uidb64>/<token>', views.change_email_success, name='change_email_success'),
    path('change/password/', views.change_password, name='change_password'),
]