from django.db import models
from common.models import CommonModel

# Create your models here.
class Room(CommonModel):
    """
        Model Definition for Houses
    """
    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = "shared_room", "Shared Room"

    name = models.CharField(
        max_length=140,
        default="",
    )
    price_per_night = models.PositiveIntegerField(
        verbose_name="Price",
        help_text="Positive Numbers Only?",
    )
    rooms = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    toilets = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    description = models.TextField()
    address = models.CharField(
        max_length=140,
    )
    pets_allowed =models.BooleanField(
        verbose_name="Pets Allowed",
        default=True, 
        help_text="Does this house allow pets?",
    )
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User", 
        on_delete=models.CASCADE,
        related_name="rooms",
    )
    amenities = models.ManyToManyField(
        "rooms.Amenity",
        related_name="rooms",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooms",
    )

    def __str__(self) -> str:
        return self.name
    
    def total_amenities(room):
        return room.amenities.count()
    
    def rating(room):
        count = room.reviews.count()
        if count == 0:
            return 0
        else:
            total_rating = 0
            for review in room.reviews.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating/count, 2)


class Amenity(CommonModel):
    """Amenity Definition"""
    name = models.CharField(
        max_length=150,
    )
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name