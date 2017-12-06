from django.urls import path

from .views import IndexView, ActivateView

app_name = 'register'
urlpatterns = [
    path('activate/<slug:token>/', ActivateView.as_view(), name='activate'),
    path('', IndexView.as_view(), name='index'),
]
