from django.conf import settings

from django.conf.urls.static import static

from django.urls import path, include #for upload file
from . import views #for upload file
from django.contrib.auth import views as auth_views

from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"), 
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('search/', views.search_results, name='search_results'),  
    path('subjects/<int:subject_id>/', views.subject_documents, name='subject_documents'),


    #for upload files               
    path('upload/', views.upload_file, name="upload_file"), #for upload files
    path('success/', views.success, name='success'), #for upload files
    path('files/', views.file_list, name='file_list'),  # For listing uploaded files



#for upload files
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)