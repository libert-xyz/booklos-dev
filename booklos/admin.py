from django.contrib import admin

from .models import *

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp','check_status']
    ordering = ['-timestamp']


admin.site.register(books, BookAdmin)
admin.site.register(categories)
