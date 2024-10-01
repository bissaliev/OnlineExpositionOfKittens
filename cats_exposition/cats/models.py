from django.contrib.auth import get_user_model
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
