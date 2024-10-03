from cats.models import Breed, Cat, Rating
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import ModelViewSet

from .filters import CatFilter
from .permissions import AuthorOrReadOnly, OwnerOrReadOnly
from .serializers import (
    BreedSerializer,
    CatCreateSerializer,
    CatSerializer,
    RatingSerializer,
)


class CatViewSet(ModelViewSet):
    """ViewSet для работы с котиками."""

    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CatFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return CatCreateSerializer
        return super().get_serializer_class()


class BreedViewSet(ModelViewSet):
    """ViewSet для работы с породами котиков."""

    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        cat = get_object_or_404(Cat, pk=self.kwargs.get("cat_id"))
        return super().get_queryset().filter(cat=cat)

    def perform_create(self, serializer):
        cat = get_object_or_404(Cat, pk=self.kwargs.get("cat_id"))
        serializer.save(user=self.request.user, cat=cat)
