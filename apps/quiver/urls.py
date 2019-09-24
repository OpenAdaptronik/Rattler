from django.urls import path
from apps.quiver import views

app_name = 'quiver'
urlpatterns = [
    path('', views.MyAnalyticsService.as_view(), name ='index'),
    path('page/<int:page>', views.MyAnalyticsService.as_view(), name='index_paginated'),
    path('new/', views.NewAnalyticsService.as_view(), name='new'),
    path('detail/<str:name>/<int:id>', views.AnalyticsServiceDetail.as_view(), name='detail'),
    path('edit/<int:id>', views.UpdateAnalyticsService.as_view(), name='edit'),
    path('delete/<int:analytics_service_id>', views.delete_analytics_service, name='deleteAnalyticsService'),
    path('execute_service/<int:analytics_service_id>', views.execute_service, name='execute_service'),

]
