from django.contrib import admin
from .models import Room

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "address",
        ("price_per_night", "pets_allowed"),
    )
    list_display = (
        "name", "price_per_night", "address", "pets_allowed"                                                                                                                                                        
    )
    list_filter = ("price_per_night", "pets_allowed")
    search_fields = ("address",)
    list_display_links = ("name", "address")
    list_editable = ("pets_allowed",)