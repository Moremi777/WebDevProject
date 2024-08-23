from django.contrib import admin
from .models import User, Moderator, Educator


class UserAdmin(admin.ModelAdmin):

    list_display=('username','email','is_staff')
    search_fields =('username','email','is_staff')
    list_per_page=25
    

admin.site.register(User, UserAdmin)

class ModeratorAdmin(admin.ModelAdmin):
    list_display = ('user', 'affiliation', 'profile_picture')
    search_fields = ('user__username', 'affiliation')

class EducatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'affiliation', 'profile_picture')
    search_fields = ('user__username', 'affiliation')
    filter_horizontal = ('subjects',)  # To add a multi-select widget for subjects

admin.site.register(Moderator, ModeratorAdmin)
admin.site.register(Educator, EducatorAdmin)
