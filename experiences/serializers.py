from rest_framework import serializers
from .models import Perk, Experience


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__" 


class ExperienceSerializer(serializers.ModelSerializer):

    is_owner = serializers.SerializerMethodField()
    class Meta:
        model = Experience
        fields = (
            "country",
            "city",
            "name",
            "host",
            "price",
            "address",
            "start",
            "end",
            "is_owner",
        )
    
    def get_is_owner(self, experience):
        request = self.context['request']
        return experience.host == request.user
