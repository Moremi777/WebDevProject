from django.conf import settings

from django.conf.urls.static import static

from django.urls import path, include #for upload file
from . import views #for upload file
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.home, name="home"), 
    #for upload files               
    path('upload/', views.upload_file, name="upload_file"),#for upload files
    path('success/', views.success, name='success'),  # for upload files
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #for upload files
]


#for upload files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
