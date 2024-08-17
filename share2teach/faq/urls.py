from django.conf import settings
from django.conf.urls.static import static
from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.faq_list, name='faq_list'),
    path('<int:pk>/', views.faq_detail, name='faq_detail'),
    path('create/', views.faq_create, name='faq_create'),
    path('<int:pk>/edit/', views.faq_update, name='faq_update'),
]