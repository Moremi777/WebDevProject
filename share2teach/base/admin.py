from django.contrib import admin
from rest_framework.permissions import BasePermission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class UserAdmin(BaseUserAdmin):
    model = CustomUser
    # Add your custom UserAdmin configuration here
admin.site.register(CustomUser)

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'admin'
