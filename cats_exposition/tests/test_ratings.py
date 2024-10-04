import pytest
from cats.models import Rating
from django.urls import reverse

from .utils import check_paginator


class TestRatingAPI:
    @pytest.mark.parametrize(
        "name, method, status",
        [
            ("rating_list", "get", 200),
            ("rating_detail", "get", 200),
            ("rating_list", "post", 401),
            ("rating_detail", "patch", 401),
            ("rating_detail", "delete", 401),
        ],
    )
    @pytest.mark.django_db
    def test_pages_availability_for_anonymous_users(
        self, client, urls, name, method, status
    ):
        url = urls[name]
        # response = client.get(url)
        response = getattr(client, method)(url)
        assert response.status_code == status, (
            f"Проверьте, что при {method.upper()} запросе `{url}` "
            f"без токена авторизации возвращается статус {status}"
        )

    @pytest.mark.parametrize(
        "name, method", [("rating_list", "post"), ("rating_detail", "put")]
    )
    @pytest.mark.django_db
    def test_request_with_incorrect_data(
        self, name, method, admin_client, urls
    ):
        url = urls[name]
        data = {}
        response = getattr(admin_client, method)(url, data=data)
        assert response.status_code == 400, (
            f"Проверьте, что при {method.upper()} запросе `{url}` "
            "с не правильными данными возвращает статус 400"
        )

    @pytest.mark.parametrize(
        "name, method, status, count",
        [
            ("rating_detail", "patch", 200, 1),
            ("rating_detail", "delete", 204, 0),
        ],
    )
    @pytest.mark.django_db
    def test_pages_availability_for_author(
        self, admin_client, name, method, status, ratings_data, urls, count
    ):
        url = urls[name]
        if method == "delete":
            response = getattr(admin_client, method)(url)
        else:
            response = getattr(admin_client, method)(url, data=ratings_data)
        assert response.status_code == status, (
            f"Проверьте, что при {method.upper()} на `{url}` пользователь "
            "может изменять или удалять свой рейтинг возвращается статус. "
            f"Ожидаемый статус ответа {status}."
        )
        assert Rating.objects.count() == count, (
            f"Проверьте, что {method.upper()} запрос `{url}` "
            "правильно изменяет данные в БД."
        )

    @pytest.mark.django_db
    def test_can_be_rated_by_auth_user(self, admin_client, cat):
        url = reverse("api:rating-list", args=[cat.id])
        response = admin_client.post(url, data={"score": 5})
        assert response.status_code == 201, (
            f"Проверьте, что при POST запросе {url} пользователем с токенов "
            "авторизации возвращается статус ответа 201"
        )
        assert Rating.objects.count() == 1, (
            f"Проверьте, что POST запрос `{url}` правильно "
            "изменяет данные в БД."
        )

    @pytest.mark.django_db
    def test_cannot_be_rated_by_owner_of_cat(self, owner_client, cat):
        url = reverse("api:rating-list", args=[cat.id])
        response = owner_client.post(url, data={"score": 5})
        assert response.status_code == 400, (
            f"Проверьте, что при POST запросе {url} владельцем котика "
            "возвращается статус ответа 400"
        )

    @pytest.mark.django_db
    def test_correct_display_on_page(self, admin_client, rating):
        url = reverse("api:rating-list", args=[rating.cat.id])
        response = admin_client.get(url)
        assert response.status_code == 200
        data = response.json()
        check_paginator(data, url)
        obj = data["results"][0]
        message = (
            "Значение параметра `results` неправильное, значение `{}` "
            "неправильное или не сохранилось при POST запросе."
        )
        assert obj.get("id") == rating.id, message.format("id")
        assert obj.get("cat") == rating.cat.name, message.format("cat")
        assert obj.get("user") == rating.user.username, message.format("user")
        assert obj.get("score") == rating.score, message.format("score")
