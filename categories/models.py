from django.db import models
from common.models import CommonModel


class CategoryChoice(models.TextChoices):
    ROOMS  = "rooms", "Rooms"
    EXPERIENCES = "experiences", "Experiences"


class category(CommonModel):
    """ Room or experience Category """
    name = models.CharField(
        max_length=50,
    )
    kind = models.CharField(
        max_length=15,
        choices=CategoryChoice.choices,
    )

    def __str__(self) -> str:
        return f"{self.kind.title()}: {self.name}"
    
    class Meta:
        verbose_name_plural = "Categories"



