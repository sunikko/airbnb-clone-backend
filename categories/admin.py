from django.contrib import admin
from .models import category


@admin.register(category)
class CategoryAdmin(admin.ModelAdmin):
    
    list_display = (
        "name",
        "kind",
    )
    list_filter = (
        "kind",
    )