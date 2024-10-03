from django.urls import include, path
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
