import pytest
from cats.models import Breed, Cat, Rating
from django.urls import reverse


@pytest.fixture
def owner(django_user_model):
    return django_user_model.objects.create_user(username="author")


@pytest.fixture
def token_owner(owner):
    from rest_framework_simplejwt.tokens import AccessToken

    token = AccessToken.for_user(owner)
    return {"access": str(token)}


@pytest.fixture
def owner_client(token_owner):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_owner['access']}")
    return client


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username="user")


@pytest.fixture
def token_user(user):
    from rest_framework_simplejwt.tokens import AccessToken

    token = AccessToken.for_user(user)
    return {"access": str(token)}


@pytest.fixture
def user_client(token_user):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_user['access']}")
    return client


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_superuser(username="admin")


@pytest.fixture
def token_admin(admin):
    from rest_framework_simplejwt.tokens import AccessToken

    token = AccessToken.for_user(admin)
    return {"access": str(token)}


@pytest.fixture
def admin_client(token_admin):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_admin['access']}")
    return client


@pytest.fixture
def breed():
    return Breed.objects.create(name="test_breed")


@pytest.fixture
def cat(owner, breed):
    return Cat.objects.create(
        name="test_cat",
        owner=owner,
        color="black",
        birth_date="2020-01-01",
        breed=breed,
    )


@pytest.fixture
def rating(cat, admin):
    return Rating.objects.create(cat=cat, user=admin, score=1)


@pytest.fixture
def cats_data(breed):
    return {
        "name": "New cat",
        "color": "Red",
        "birth_date": "2016-12-12",
        "breed": breed.name,
        "description": "Cool cat",
    }


@pytest.fixture
def breeds_data():
    return {"name": "New Breed"}


@pytest.fixture
def ratings_data():
    return {"score": 5}


@pytest.fixture
def urls(cat, breed, rating):
    data_urls = {
        "cat_list": reverse("api:cat-list"),
        "cat_detail": reverse("api:cat-detail", args=[cat.id]),
        "breed_list": reverse("api:breed-list"),
        "breed_detail": reverse("api:breed-detail", args=[breed.id]),
        "rating_list": reverse("api:rating-list", args=[cat.id]),
        "rating_detail": reverse(
            "api:rating-detail", args=[cat.id, rating.id]
        ),
    }
    return data_urls


@pytest.fixture
def filters_params(cat):
    return {"breed": cat.breed.name, "owner": cat.owner.username, "rating": 0}
