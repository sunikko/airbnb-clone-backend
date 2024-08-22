from rest_framework import serializers
from .models import category


class CategorySerializer(serializers.Serializer):

    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True,
        max_length=50,    
    )
    kind = serializers.ChoiceField(
        choices=category.CategoryKindChoices.choices,
    )
    created_at = serializers.DateTimeField(read_only=True)


    def create(self, validated_data):
        return category.objects.create(**validated_data)