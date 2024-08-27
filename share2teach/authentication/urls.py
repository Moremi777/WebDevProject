from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path("logout_user", views.logout_user, name='logout_user'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_register/', views.admin_register, name='admin_register'),
    path("logout_admin", views.logout_admin, name='logout_admin'),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]