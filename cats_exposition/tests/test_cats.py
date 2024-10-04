from datetime import datetime

import pytest
from api.utils import calculating_age_in_months
from cats.models import Cat, Rating
from django.urls import reverse

from .utils import check_paginator


class TestCatAPI:
    @pytest.mark.parametrize(
        "name, method, status",
        [
            ("cat_list", "get", 200),
            ("cat_detail", "get", 200),
            ("cat_list", "post", 401),
            ("cat_detail", "patch", 401),
            ("cat_detail", "delete", 401),
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
        "method, status",
        [("patch", 403), ("delete", 403)],
    )
    @pytest.mark.django_db
    def test_pages_availability_for_not_owner(
        self, admin_client, urls, method, status
    ):
        url = urls["cat_detail"]
        response = getattr(admin_client, method)(url)
        assert response.status_code == status, {
            f"Проверьте, что при {method.upper()} запросе `{url}` "
            f"от другого пользователя возвращается статус {status}"
        }

    @pytest.mark.parametrize(
        "name, method", [("cat_list", "post"), ("cat_detail", "put")]
    )
    @pytest.mark.django_db
    def test_request_with_incorrect_data(
        self, name, method, owner_client, urls
    ):
        message = (
            "Проверьте, что при {} запросе `{}` с не правильными "
            "данными возвращает статус 400"
        )
        url = urls[name]
        data = {}
        response = getattr(owner_client, method)(url, data=data)
        assert response.status_code == 400, message.format(method.upper(), url)

    @pytest.mark.parametrize(
        "name, method, status, count",
        [
            ("cat_list", "post", 201, 2),
            ("cat_detail", "patch", 200, 1),
            ("cat_detail", "delete", 204, 0),
        ],
    )
    @pytest.mark.django_db
    def test_pages_availability_for_owner(
        self, owner_client, name, method, status, cats_data, urls, count
    ):
        message = (
            "Проверьте, что при {} запросе `{}` "
            "пользователем с токеном авторизации возвращается статус {}"
        )
        url = urls[name]
        if method == "delete":
            response = getattr(owner_client, method)(url)
        else:
            response = getattr(owner_client, method)(url, data=cats_data)
        assert response.status_code == status, message.format(
            method.upper(), url, status
        )
        message = (
            "Проверьте, что {} запрос `{}` правильно изменяет данные в БД."
        )
        assert Cat.objects.count() == count, message.format(
            method.upper(), url
        )

    @pytest.mark.parametrize(
        "name, method", [("cat_list", "post"), ("cat_detail", "patch")]
    )
    @pytest.mark.django_db
    def test_saving_correct_data(
        self, owner_client, cats_data, urls, name, method
    ):
        url = urls[name]
        getattr(owner_client, method)(url, data=cats_data)
        cat = Cat.objects.filter(name=cats_data.get("name"))[0]
        msg = (
            f"Проверьте, что при {method.upper()} запросе `{url}` "
            "правильно сохраняются в БД значение "
        )
        assert cat.name == cats_data["name"], msg + "`name`."
        assert cat.color == cats_data["color"], msg + "`color`."
        assert cat.description == cats_data["description"], (
            msg + "`description`."
        )
        assert cat.birth_date.isoformat() == cats_data["birth_date"], (
            msg + "`birth_date`."
        )
        assert cat.breed.name == cats_data["breed"], msg + "`breed`."

    @pytest.mark.django_db
    def test_correct_display_on_page(self, owner_client, cat, admin):
        url = reverse("api:cat-list")
        response = owner_client.get(url)
        assert response.status_code == 200
        data = response.json()
        check_paginator(data, url)
        obj = data["results"][0]
        message = (
            "Значение параметра `results` неправильное, значение `{}` "
            "неправильное или не сохранилось при POST запросе."
        )
        assert obj.get("id") == cat.id, message.format("id")
        assert obj.get("name") == cat.name, message.format("name")
        assert obj.get("color") == cat.color, message.format("color")
        assert obj.get("breed") == cat.breed.name, message.format("breed")
        assert obj.get("description") == cat.description, message.format(
            "description"
        )
        birth_date = datetime.strptime(cat.birth_date, "%Y-%m-%d")
        age = calculating_age_in_months(birth_date)
        assert obj.get("age") == age, message.format("age")
        assert obj.get("rating") == 0, message.format("rating")
        Rating.objects.create(cat=cat, user=admin, score=5)
        response = owner_client.get(url)
        assert response.status_code == 200
        data = response.json()
        obj = data["results"][0]
        assert obj.get("rating") == 5, message.format("rating")

    @pytest.mark.django_db
    def test_uniqueness_for_owner_name(self, owner_client, cats_data):
        url = reverse("api:cat-list")
        response = owner_client.post(url, data=cats_data)
        assert response.status_code == 201
        response = owner_client.post(url, data=cats_data)
        assert response.status_code == 400, (
            f"Проверьте, что при POST запросе {url} сохраняется "
            "уникальность `owner - name`."
        )

    @pytest.mark.parametrize("param", ["breed", "owner", "rating"])
    @pytest.mark.django_db
    def test_filter_correct(self, owner_client, param, filters_params):
        url = reverse("api:cat-list")
        response = owner_client.get(f"{url}?{param}={filters_params[param]}")
        assert response.status_code == 200, (
            f"Проверьте, что при GET запросе {url} "
            f"по фильтру `{param}` статус ответа 200."
        )
        assert len(response.json()["results"]) == 1, (
            f"Проверьте, что при GET запросе {url} "
            f"по фильтру `{param}` возвращается правильный результат."
        )
