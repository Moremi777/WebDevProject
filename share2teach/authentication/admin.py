from django.contrib import admin
from .models import User, Educator, Moderator, Subject

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'user_type')
    search_fields = ('username', 'email', 'user_type')
    list_per_page = 25

admin.site.register(User, UserAdmin)
admin.site.register(Educator)
admin.site.register(Moderator)
admin.site.register(Subject)
