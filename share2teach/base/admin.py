from django.contrib import admin
from .models import Subject

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Subject, SubjectAdmin)
#from rest_framework.permissions import BasePermission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class UserAdmin(BaseUserAdmin):
    model = CustomUser
    # Add your custom UserAdmin configuration here
admin.site.register(CustomUser)
