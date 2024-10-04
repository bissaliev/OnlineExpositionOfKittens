import pytest
from cats.models import Breed
from django.urls import reverse

from .utils import check_paginator


class TestBreedAPI:
    @pytest.mark.parametrize(
        "name, method, status",
        [
            ("breed_list", "get", 200),
            ("breed_detail", "get", 200),
            ("breed_list", "post", 401),
            ("breed_detail", "patch", 401),
            ("breed_detail", "delete", 401),
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
        "name, method",
        [
            ("breed_list", "post"),
            ("breed_detail", "patch"),
            ("breed_detail", "delete"),
        ],
    )
    @pytest.mark.django_db
    def test_pages_availability_for_not_admin(
        self, owner_client, urls, name, method
    ):
        url = urls[name]
        response = getattr(owner_client, method)(url)
        assert response.status_code == 403, (
            f"Проверьте, что при {method.upper()} запросе `{url}` пользователем"
            " со свойством `is_staff=False' возвращается статус 403"
        )

    @pytest.mark.parametrize(
        "name, method", [("breed_list", "post"), ("breed_detail", "put")]
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
            ("breed_list", "post", 201, 2),
            ("breed_detail", "patch", 200, 1),
            ("breed_detail", "delete", 204, 0),
        ],
    )
    @pytest.mark.django_db
    def test_pages_availability_for_admin(
        self, admin_client, name, method, status, breeds_data, urls, count
    ):
        url = urls[name]
        if method == "delete":
            response = getattr(admin_client, method)(url)
        else:
            response = getattr(admin_client, method)(url, data=breeds_data)
        assert response.status_code == status, (
            f"Проверьте, что при {method.upper()} на `{url}` пользователем "
            f"со свойством `is_staff=True` возвращается статус {status}"
        )
        assert Breed.objects.count() == count, (
            f"Проверьте, что {method.upper()} запрос `{url}` "
            "правильно изменяет данные в БД."
        )

    @pytest.mark.django_db
    def test_correct_display_on_page(self, owner_client, breed):
        url = reverse("api:breed-list")
        response = owner_client.get(url)
        assert response.status_code == 200
        data = response.json()
        check_paginator(data, url)
        obj = data["results"][0]
        message = (
            "Значение параметра `results` неправильное, значение `{}` "
            "неправильное или не сохранилось при POST запросе."
        )
        assert obj.get("id") == breed.id, message.format("id")
        assert obj.get("name") == breed.name, message.format("name")

    @pytest.mark.parametrize(
        "name, method", [("breed_list", "post"), ("breed_detail", "patch")]
    )
    @pytest.mark.django_db
    def test_saving_correct_data(
        self, admin_client, breeds_data, urls, name, method
    ):
        url = urls[name]
        getattr(admin_client, method)(url, data=breeds_data)
        breed = Breed.objects.filter(name=breeds_data.get("name"))[0]
        assert breed.name == breeds_data["name"], (
            f"Проверьте, что при {method.upper()} запросе `{url}` "
            "правильно сохраняются в БД значение `name`"
        )

    @pytest.mark.django_db
    def test_uniqueness_for_owner_name(self, admin_client, breeds_data):
        url = reverse("api:breed-list")
        response = admin_client.post(url, data=breeds_data)
        assert response.status_code == 201
        response = admin_client.post(url, data=breeds_data)
        assert response.status_code == 400, (
            f"Проверьте, что при POST запросе {url} сохраняется "
            "уникальность `name`."
        )
