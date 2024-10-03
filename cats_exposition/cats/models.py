from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_birth_date

User = get_user_model()


class Breed(models.Model):
    """Порода."""

    name = models.CharField("Название породы", max_length=150, unique=True)

    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = "Породы"

    def __str__(self):
        return self.name


class Cat(models.Model):
    """Котики."""

    name = models.CharField("Имя котика", max_length=150)
    color = models.CharField("Цвет котика", max_length=150)
    birth_date = models.DateField(
        "Дата рождения котика", validators=[validate_birth_date]
    )
    description = models.TextField("Описание котика")
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cats",
        verbose_name="Хозяин котика",
    )
    breed = models.ForeignKey(
        Breed,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cats",
        verbose_name="Порода котика",
    )

    class Meta:
        verbose_name = "Котик"
        verbose_name_plural = "Котики"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "owner"],
                name="unique_name_owner",
            )
        ]

    def __str__(self):
        return self.name


class Rating(models.Model):
    """Рейтинг котиков."""

    cat = models.ForeignKey(
        Cat, on_delete=models.CASCADE, related_name="ratings"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="ratings"
    )
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1, "Оценка должна быть в диапазоне от 1 до 5"),
            MaxValueValidator(5, "Оценка должна быть в диапазоне от 1 до 5"),
        ],
    )

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
        constraints = [
            models.UniqueConstraint(
                fields=["cat", "user"], name="unique_rating"
            )
        ]

    def __str__(self):
        return (
            f"Пользователь {self.user.username} поставил "
            f"котику {self.cat.name} оценку {self.score}"
        )

    def clean(self) -> None:
        if self.user == self.cat.owner:
            raise ValidationError("Нельзя оценивать своего котика!")

    def save(self, *args, **kwargs) -> None:
        self.clean()
        super().save(*args, **kwargs)
