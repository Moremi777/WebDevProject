from django.contrib import admin
from .models import Subject,Subjects
''''from .models import UploadedFile'''


'''class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'name',)
    search_fields = ('uploaded_at',)'''
   

'''admin.site.register(UploadedFile, UploadedFileAdmin)'''
#from rest_framework.permissions import BasePermission



admin.site.register(Subjects)



