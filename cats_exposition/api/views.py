from cats.models import Breed, Cat
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from .filters import CatFilter
from .permissions import OwnerOrReadOnly
from .serializers import BreedSerializer, CatSerializer


class CatViewSet(ModelViewSet):
    """ViewSet для работы с котиками."""

    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CatFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BreedViewSet(ModelViewSet):
    """ViewSet для работы с породами котиков."""

    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
