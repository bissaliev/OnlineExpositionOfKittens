from api.utils import calculating_age_in_months
from django.contrib import admin
from django.db.models import Avg
from django.db.models.functions import Coalesce

from .models import Breed, Cat, Rating

admin.site.register(Breed)


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "color",
        "breed",
        "birth_date",
        "owner",
        "avg_rating",
        "age",
    )
    list_editable = ("color", "breed", "owner")
    list_display_links = ("id", "name")
    list_filter = ("breed", "owner")
    search_fields = ("name", "color", "owner__username", "breed__name")

    @admin.display(description="Средний рейтинг")
    def avg_rating(self, obj):
        return obj.ratings.aggregate(avg_rating=Coalesce(Avg("score"), 0.0))[
            "avg_rating"
        ]

    @admin.display(description="Возраст")
    def age(self, obj):
        return calculating_age_in_months(obj.birth_date)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "cat", "cat__owner", "user", "score")
    list_editable = ("cat", "user", "score")
    list_display_links = ("id",)
    list_filter = ("cat", "user")
    search_fields = ("cat__name", "user__username")
