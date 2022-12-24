from django.contrib import admin

from .models import Review


@admin.register(Review)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'text', 'created']
    list_filter = ['user']
    list_display_links = ['user', 'text']
