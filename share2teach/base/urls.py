from django.conf import settings
<<<<<<< HEAD
from django.conf.urls.static import static
=======
from django.conf.urls.static import static 
>>>>>>> fd96fa894f51faa6a89861552f97c3c68ac90a1d
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path("", views.home, name="home"), 
<<<<<<< HEAD
    path("register/", views.register, name="register" ),
    path("login/", views.login, name="login")
    #for upload files
    path('admin/', admin.site.urls),
    path('upload/', include('fileupload.urls')),
]


#for upload files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('', include(router.urls)),
]

>>>>>>> fd96fa894f51faa6a89861552f97c3c68ac90a1d
