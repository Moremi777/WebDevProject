from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"), 
    path("register/", views.register, name="register" ),
    path("login/", views.login, name="login")
    #for upload files
    path('admin/', admin.site.urls),
    path('upload/', include('fileupload.urls')),
]


#for upload files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)