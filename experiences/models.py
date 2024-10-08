from django.db import models
from common.models import CommonModel


class Experience(CommonModel):
    """Experience Model Definition"""
    country = models.CharField(
        max_length=50,
        default="UK",
    )
    city = models.CharField(
        max_length=80,
        default="London",
    )
    name = models.CharField(
        max_length=255,
    )
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    price = models.PositiveIntegerField()
    address = models.CharField(
        max_length=255,
    )
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField(
        "experiences.Perk",
        related_name="experiences",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="experiences",
    )

    def __str__(self) -> str:
        return self.name


class Perk(CommonModel):
    """ What is included on an Experience """
    name = models.CharField(
        max_length=100,
    )
    details = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )
    explanation = models.TextField(
        blank=True,
        default="",
    )

    def __str__(self) -> str:
        return self.name
