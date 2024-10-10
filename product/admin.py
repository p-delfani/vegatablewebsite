from django.contrib import admin
from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')


admin.site.register(models.Category)
admin.site.register(models.Size)
