from django.db import models

# Create your models here.
class Room(models.Model):
    """
        Model Definition for Houses
    """
    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = "shared_room", "Shared Room"

    name = models.CharField(
        max_length=140,
    )
    price_per_night = models.PositiveIntegerField(
        verbose_name="Price",
        help_text="Positive Numbers Only?",
    )
    roooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(
        max_length=140,
    )
    pets_allowed =models.BooleanField(
        verbose_name="Pets Allowed?",
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
    )

    def __str__(self):
        return self.name
    

class Amenity(models.Model):
    """Amenity Definition"""
    name = models.CharField(
        max_length=150,
    )
    description = models.CharField(
        max_length=150,
        null=True,
    )