from django.conf import settings
from django.conf.urls.static import static 
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
'''from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet) path('api/', include(router.urls)),'''

urlpatterns = [
    path("", views.home, name="home"), 
]

