from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")
    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")
    class CurrencyChoices(models.TextChoices):
        WON = "won", "Korean Won"
        USD = "gbp", "Pound"

    first_name = models.CharField(
        max_length=150, 
        editable=False,
    )
    last_name = models.CharField(
        max_length=150, 
        editable=False,
    )
    name = models.CharField(
        max_length=150, 
        default="",
    )
    is_host = models.BooleanField(
        default=False,
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
        default="en"
    )
    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoices.choices,
        default="gbp",
    )
    avatar = models.URLField(
        blank=True,
    )