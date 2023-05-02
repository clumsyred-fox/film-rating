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
from .permissions import (IsAdminModeratorOwnerOrReadOnly,
                          IsAdminOrReadOnly)


class CreateListDestroyViewSet(ListModelMixin,
                               CreateModelMixin,
                               DestroyModelMixin,
                               GenericViewSet):
    """ Кастомный миксин. """
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    """ Вьюсет для Категорий. """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(CreateListDestroyViewSet):
    """ Вьюсет для Жанров. """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TitleGETViewSet(viewsets.ModelViewSet):
    """ Вьюсет для Произведений. """
    queryset = Title.objects.all()
    serializer_class = TitleGETSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TitlePOSTSerializer
        else:
            return TitleGETSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ Вьюсет для Отзывов. """
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
    """ Вьюсет для Комментариев. """
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
