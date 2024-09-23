from django.conf import settings

from django.conf.urls.static import static

from django.urls import path, include 
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include

from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from django.shortcuts import render
from .views import user_subject_view #code for user subject

from prometheus_client import make_wsgi_app
from django.http import HttpResponse


urlpatterns = [
    path("", views.home, name="home"), 
    path('search/', views.search_results, name='search_results'),  
    path('upload/', views.upload_document, name='upload_document'),
    path('documents/', views.document_list, name='document_list'),
    path('document/<int:document_id>/', views.document_detail, name='document_detail'),
    path('upload/', views.upload_document, name='upload_document'), 
    path('document/<int:id>/', views.document_detail, name='document_detail'),
    path('documents/<int:document_id>/report/', views.report_document, name='report_document'),
    #for upload files
    #path('subjects/<int:subject_id>/', views.subject_documents, name='subject_documents'),
    path('subjects/',views.subjects, name = 'subjects'),
    path('subjects/<int:subject_id>/', views.selected_subject, name='selected_subject'),
    path('oauth/', views.google_oauth, name='google_oauth'),
    #path('subjects/<int:subject_id>/', views.subject_documents, name='subject_documents'),'''

    path('select-subject/', user_subject_view, name='select_subject'),
    path('oauth/', views.google_oauth, name='google_oauth'),

    #for upload files               
    path('upload/', views.upload_file, name="upload_file"), #for upload files
    path('success/', views.success, name='success'), #for upload files
    path('files/', views.file_list, name='file_list'),  # For listing uploaded files
 

    #path('report/<int:document_id>/', views.report_document, name='report_document'), # MOREMI FILE REPORTING
    path('metrics/', views.metrics_view),

]


#for upload files
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


