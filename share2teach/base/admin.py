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

admin.site.register(Document)



    # Custom method to display image in admin
def image_display(self, obj):
    if obj.image:
        return f"<img src='{obj.image.url}' style='width: 50px; height: 50px;'/>"
    else:
        return 'No image'
image_display.allow_tags = True
image_display.short_description = 'Contributor Image'

#admin.site.register(Contributor, ContributorAdmin)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Adjust fields as per your model
    search_fields = ('name',)  # Filters for the admin panel

admin.site.register(Subject, SubjectAdmin)


#from rest_framework.permissions import BasePermission



