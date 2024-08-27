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
    path('report/<int:document_id>/', views.report_document, name='report_document'), # MOREMI FILE REPORTING
    path('admin/messages/', views.view_messages, name='view_messages'), # MOREMI FILE REPORTING MESSAGE
    path('admin/messages/delete/<int:message_id>/', views.delete_message, name='delete_message'), # MOREMI FILE REPORTING MESSAGE
    path('admin/messages/mark-read/<int:message_id>/', views.mark_message_as_read, name='mark_message_as_read'), # MOREMI FILE REPORTING MESSAGE
    path('admin/messages/', views.view_messages, name='view_messages'), # MOREMI FILE REPORTING MESSAGE
    path('admin/messages/delete/<int:message_id>/', views.delete_message, name='delete_message'), # MOREMI FILE REPORTING MESSAGE

]

