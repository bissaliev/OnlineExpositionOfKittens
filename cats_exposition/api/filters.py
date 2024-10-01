from cats.models import Cat
from django_filters import rest_framework as filters


class CatFilter(filters.FilterSet):
    """Фильтр котиков."""

    breed = filters.CharFilter(field_name="breed__name")
    owner = filters.CharFilter(field_name="owner__username")

    class Meta:
        model = Cat
        fields = ("breed", "color", "owner")
