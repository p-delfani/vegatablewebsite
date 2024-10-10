from django.contrib import admin
from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('updated_at',)
    search_fields = ('title', 'body')


@admin.register(models.BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user')
