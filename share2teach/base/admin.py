from django.contrib import admin
from .models import Subject, Report, Document
   
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


#from rest_framework.permissions import BasePermission

admin.site.register(Subject)
admin.site.register(Document)



