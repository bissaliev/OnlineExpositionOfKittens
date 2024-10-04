from cats.models import Breed, Cat, Rating
from rest_framework import serializers

from .utils import calculating_age_in_months


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
        birth_date = obj.birth_date
        age = calculating_age_in_months(birth_date)
        return age


class RatingSerializer(serializers.ModelSerializer):
    """Сериализатор для рейтинга котиков."""

    cat = serializers.SlugRelatedField(read_only=True, slug_field="name")
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    score = serializers.IntegerField(required=True)

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
