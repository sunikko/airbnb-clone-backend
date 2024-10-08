from django.contrib import admin
from .models import Room, Amenity

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "name", 
        "price_per_night",
        "kind",
        "total_amenities",
        "owner",
        "address", 
        "pets_allowed",
        "rating",
        "created_at",
        "updated_at",                                                                                                                                                        
    )
    list_filter = (
        "price_per_night", 
        "pets_allowed",
        "kind",
        "amenities",
        "created_at",
        "updated_at",
    )
    search_fields = ("address",)
    list_display_links = ("name", "address")
    list_editable = ("pets_allowed",)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )