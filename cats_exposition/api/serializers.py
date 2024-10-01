from datetime import date

from cats.models import Breed, Cat
from rest_framework import serializers


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = (
            "id",
            "name",
        )


class CatSerializer(serializers.ModelSerializer):
    breed = serializers.SlugRelatedField(
        queryset=Breed.objects.all(), slug_field="name"
    )
    owner = serializers.SlugRelatedField(read_only=True, slug_field="username")
    age = serializers.SerializerMethodField()

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
            "age",
        )

    def get_age(self, obj: Cat):
        today = date.today()
        birth_date = obj.birth_date
        years_diff = today.year - birth_date.year
        months_diff = today.month - birth_date.month
        total_month = years_diff * 12 + months_diff
        if today.day < birth_date.day:
            total_month -= 1
        return total_month
