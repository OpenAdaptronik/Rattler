from django.urls import path, reverse
from django.contrib.auth import views as auth_views
from django.utils.functional import lazy

reverse_lazy = lazy(reverse, str)

app_name = 'password'
urlpatterns = [
    path(
        'forget/',
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy('password:forget_done')
        ), 
        name='forget'
    ),
    path(
        'forget/done/', 
        auth_views.PasswordResetDoneView.as_view(),
        name='forget_done'
    ),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.
         as_view(success_url=reverse_lazy('password:reset_done')), name='reset'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='reset_done'),
]
