from cats.models import Breed, Cat
from rest_framework import serializers


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ("name",)


class CatSerializer(serializers.ModelSerializer):
    breed = serializers.SlugRelatedField(
        queryset=Breed.objects.all(), slug_field="name"
    )
    owner = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Cat
        fields = (
            "id",
            "name",
            "color",
            "owner",
            "breed",
            "birth_date",
            "description",
        )
