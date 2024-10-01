from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("auth/", include("djoser.urls")),
    # JWT-эндпоинты, для управления JWT-токенами
    path("auth/", include("djoser.urls.jwt")),
]

# Эндпоинты аутентификации:
# auth/users/ - регистрация нового пользователя
# auth/users/me/ - получить/обновить зарегистрированного пользователя
# auth/jwt/create/ - создать токен
# auth/jwt/refresh/ - получить новый токен по истечению времени жизни старого
