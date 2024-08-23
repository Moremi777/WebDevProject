from django.contrib import admin
from .models import FAQ

# Register your models here.

#The FAQ ON THE ADMIN SITE
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'status', 'date_created')
    list_filter = ('status', 'category')
    search_fields = ('question', 'answer', 'category')
