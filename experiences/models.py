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
    )
    price = models.PositiveIntegerField()
    address = models.CharField(
        max_length=255,
    )
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    # perks = 