from datetime import date

from cats.models import Breed, Cat, Rating
from rest_framework import serializers


class BreedSerializer(serializers.ModelSerializer):
    """Сериализатор пород котиков."""

    class Meta:
        model = Breed
        fields = (
            "id",
            "name",
        )


class BaseCatSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для котиков."""

    breed = serializers.SlugRelatedField(
        queryset=Breed.objects.all(), slug_field="name"
    )
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Cat
        fields = (
            "id",
            "name",
            "color",
            "breed",
            "description",
            "owner",
        )


class CatCreateSerializer(BaseCatSerializer):
    """Сериализатор для создания котиков."""

    class Meta(BaseCatSerializer.Meta):
        fields = BaseCatSerializer.Meta.fields + ("birth_date",)
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Cat.objects.all(),
                fields=("name", "owner"),
                message="У вас есть уже такой котик, зачем вам второй!",
            )
        ]


class CatSerializer(BaseCatSerializer):
    """Сериализатор котиков."""

    age = serializers.SerializerMethodField()
    rating = serializers.IntegerField(source="rating_avg")

    class Meta(BaseCatSerializer.Meta):
        fields = BaseCatSerializer.Meta.fields + ("age", "rating")

    def get_age(self, obj: Cat):
        """Возвращает возраст котика в месяцах."""
        today = date.today()
        birth_date = obj.birth_date
        years_diff = today.year - birth_date.year
        months_diff = today.month - birth_date.month
        total_month = years_diff * 12 + months_diff
        if today.day < birth_date.day:
            total_month -= 1
        return total_month


class RatingSerializer(serializers.ModelSerializer):
    """Сериализатор для рейтинга котиков."""

    cat = serializers.SlugRelatedField(read_only=True, slug_field="name")
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Rating
        fields = (
            "id",
            "cat",
            "user",
            "score",
        )

    def create(self, validated_data):  # TODO Убрать дублирование исключения
        cat = validated_data.get("cat")
        user = self.context.get("request").user
        if user == cat.owner:
            raise serializers.ValidationError(
                "Нельзя оценивать своего котика!"
            )
        if Rating.objects.filter(cat=cat, user=user).exists():
            raise serializers.ValidationError("Вы уже оценили данного котика!")
        return super().create(validated_data)
