from django.conf import settings

from django.conf.urls.static import static

from django.urls import path, include 
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

'''from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet) path('api/', include(router.urls)),'''

from prometheus_client import make_wsgi_app
from django.http import HttpResponse


urlpatterns = [
    path("", views.home, name="home"), 
    path('search/', views.search_results, name='search_results'),  
    path('subjects/<int:subject_id>/', views.subject_documents, name='subject_documents'),
    path('upload/', views.upload_document, name='upload_document'),
    path('documents/', views.document_list, name='document_list'),
    path('document/<int:document_id>/', views.document_detail, name='document_detail'),
    path('upload/', views.upload_document, name='upload_document'), 
    path('document/<int:id>/', views.document_detail, name='document_detail'),
    path('documents/<int:document_id>/report/', views.report_document, name='report_document'),
    #for upload files
    path('success/', views.success, name='success'), #for upload files
    path('files/', views.file_list, name='file_list'),  # For listing uploaded files

    path('report/<int:document_id>/', views.report_document, name='report_document'), # MOREMI FILE REPORTING
    path('admin/messages/', views.view_messages, name='view_messages'), # MOREMI FILE REPORTING MESSAGE
    path('admin/messages/delete/<int:message_id>/', views.delete_message, name='delete_message'), # MOREMI FILE REPORTING MESSAGE
    path('admin/messages/mark-read/<int:message_id>/', views.mark_message_as_read, name='mark_message_as_read'), # MOREMI FILE REPORTING MESSAGE
    path('admin/messages/', views.view_messages, name='view_messages'), # MOREMI FILE REPORTING MESSAGE
    path('admin/messages/delete/<int:message_id>/', views.delete_message, name='delete_message'), # MOREMI FILE REPORTING MESSAGE

    path('metrics/', views.metrics_view),

]


#for upload files
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
