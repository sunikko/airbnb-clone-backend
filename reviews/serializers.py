from rest_framework import serializers
from users.serializers import TinyUserSerializer
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    
    user = TinyUserSerializer(read_only=True) # to show tinyuser info instead of seq number
    class Meta:
        model = Review
        # fields = "__all__"
        fields = (
            "user",
            "payload",
            "rating",
            "room",
        )
        # extra_kwargs = {
        #     'user': {'read_only': True},  # Make user field read-only
        #     'room': {'read_only': True},  # Make room field read-only
        # }
