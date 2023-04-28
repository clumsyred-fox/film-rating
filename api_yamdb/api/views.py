from rest_framework import viewsets
from rest_framework.mixins import (ListModelMixin,
                                   CreateModelMixin,
                                   DestroyModelMixin
                                   )
from rest_framework.viewsets import GenericViewSet

from reviews.models import Category, Genre, Title
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleGETSerializer,
                          TitlePOSTSerializer,
                          )


class CreateListDestroyViewSet(ListModelMixin,
                               CreateModelMixin,
                               DestroyModelMixin,
                               GenericViewSet):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleGETViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleGETSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TitlePOSTSerializer
        else:
            return TitleGETSerializer
