from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterAPIView, LoginAPIView, verify_email
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    path('register/', views.register_view, name='register'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('login/', views.login_view, name='login'),
    path('admin/admin-login/', views.admin_login_page, name='admin_login'),
    path('api/admin-login-action/', views.AdminLoginView.as_view(), name='admin_login_action'),
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('email-verified-success/', views.email_verified_success, name='email_verified_success'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('admin/dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/manage-users/', views.manage_users, name='admin_manage_users'),
    path('admin/edit-user/<int:user_id>/', views.edit_user, name='admin_edit_user'),
    path('user/<int:user_id>/delete/', views.DeleteUserView.as_view(), name='delete_user'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('admin/site-settings/', views.site_settings, name='admin_site_settings'),
    path('admin/update-site-settings/', views.update_site_settings, name='update_site_settings'),
    path('user/add/', views.add_user, name='admin_add_user'),
    path('user/<int:user_id>/edit/', views.edit_user, name='admin_edit_user'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('logout/', views.logout_view, name='logout'),
]
