from django.contrib import admin
from .models import Subject, UploadedFile


class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file',)
    search_fields = ('uploaded_at',)
   

admin.site.register(UploadedFile, UploadedFileAdmin)
#from rest_framework.permissions import BasePermission



