from django.contrib import admin
from .models import User, Educator, Moderator, Subject
from .forms import AdminUserEditForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse, path
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

class UserAdmin(BaseUserAdmin):
    form = AdminUserEditForm  # Use your custom form here

    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),  # Add the user_type field to the admin form
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'delete_button')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    list_per_page = 25

    def delete_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Delete</a>',
            reverse('admin:delete_user', args=[obj.pk])
        )
    
    delete_button.short_description = 'Delete User'
    delete_button.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:user_id>/delete/',
                self.admin_site.admin_view(self.delete_user_view),
                name='delete_user',
            ),
        ]
        return custom_urls + urls

    def delete_user_view(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        self.message_user(request, f"The user {user.username} has been deleted.")
        return HttpResponseRedirect(reverse('admin:auth_user_changelist'))

    actions = ['delete_selected_users']

    def delete_selected_users(self, request, queryset):
        for user in queryset:
            user.delete()
        self.message_user(request, "Selected users have been deleted.")
    
    delete_selected_users.short_description = "Delete selected users"

# Register your models
admin.site.register(User, UserAdmin)
admin.site.register(Educator)
admin.site.register(Moderator)
admin.site.register(Subject)
