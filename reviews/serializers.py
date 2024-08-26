from rest_framework import serializers
from users.serializers import TinyUserSerializer
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    
    user = TinyUserSerializer(read_only=True) # to show tinyuser info instead of seq number
    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating",
        )
