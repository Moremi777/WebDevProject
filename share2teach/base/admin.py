from django.contrib import admin
from .models import Subject, UploadedFile, Report


class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file',)
    search_fields = ('uploaded_at',)
   
class ReportAdmin(admin.ModelAdmin):
    list_display = ('document_title', 'document_file', 'reported_by', 'reason', 'created_at')
    search_fields = ('document__title', 'reported_by', 'reason')
    list_filter = ('created_at',)

    def document_title(self, obj):
        return obj.document.title

    def document_file(self, obj):
        return obj.document.file.url if obj.document.file else 'No file attached'

    document_title.short_description = 'Document Title'
    document_file.short_description = 'Document File'

admin.site.register(Report, ReportAdmin)

admin.site.register(UploadedFile, UploadedFileAdmin)

#from rest_framework.permissions import BasePermission



