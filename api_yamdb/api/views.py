from rest_framework.mixins import (ListModelMixin,
                                   CreateModelMixin,
                                   DestroyModelMixin
                                   )
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets

from rest_framework.viewsets import GenericViewSet
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleGETSerializer,
                          TitlePOSTSerializer,
                          CommentSerializer,
                          ReviewSerializer,
                          )
from reviews.models import Category, Genre, Review, Title, CustomUser
from .permissions import (IsAdminModeratorOwnerOrReadOnly)


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
            

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))

        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)