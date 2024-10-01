from cats.models import Breed, Cat
from rest_framework.viewsets import ModelViewSet

from .serializers import BreedSerializer, CatSerializer


class CatViewSet(ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BreedViewSet(ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
