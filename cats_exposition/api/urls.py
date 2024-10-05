from django.urls import include, path
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter

from .views import BreedViewSet, CatViewSet, RatingViewSet

app_name = "api"

router = DefaultRouter()

router.register(r"cats/(?P<cat_id>[\d]+)/rating", RatingViewSet)
router.register("cats", CatViewSet, basename="cat")
router.register("breeds", BreedViewSet, basename="breed")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls")),
    # JWT-эндпоинты, для управления JWT-токенами
    path("auth/", include("djoser.urls.jwt")),
]

# Эндпоинты аутентификации:
# auth/users/ - регистрация нового пользователя
# auth/users/me/ - получить/обновить зарегистрированного пользователя
# auth/jwt/create/ - создать токен
# auth/jwt/refresh/ - получить новый токен по истечению времени жизни старого


api_info = openapi.Info(
    title="Cats Exposition API",  # Название вашего API
    default_version="v1",  # Версия API
    description="Документация для API выставки котов",  # Описание API
    terms_of_service="https://www.example.com/terms/",  # Условия использования
    contact=openapi.Contact(
        email="support@example.com"
    ),  # Контактная информация
    license=openapi.License(name="BSD License"),  # Лицензия
)
