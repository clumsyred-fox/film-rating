from rest_framework.mixins import (ListModelMixin,
                                   CreateModelMixin,
                                   DestroyModelMixin
                                   )
from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from .filter import TitlesFilter
from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from rest_framework.viewsets import GenericViewSet
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleGETSerializer,
                          TitlePOSTSerializer,
                          CommentSerializer,
                          ReviewSerializer,
                          ObtainTokenSerializer,
                          RegistrationSerializer,
                          UserSerializer, 
                          UserEditSerializer, 
                          )
from api_yamdb.settings import FROM_EMAIL
from reviews.models import Category, Genre, Review, Title, CustomUser
from .permissions import (IsAdminModeratorOwnerOrReadOnly,
                          IsAdminOrReadOnly, IsAdmin)


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
    permission_classes = [IsAdminOrReadOnly]


class GenreViewSet(CreateListDestroyViewSet):
    """ Вьюсет для Жанров. """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleGETViewSet(viewsets.ModelViewSet):
    """ Вьюсет для Произведений. """
    queryset = Title.objects.all()
    serializer_class = TitleGETSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter


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


class AuthTokenView(APIView):
    def post(request):
        serializer = ObtainTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(CustomUser, username=serializer.validated_data["username"])

        if default_token_generator.check_token(
            user, serializer.validated_data["confirmation_code"]):
            token = RefreshToken.for_user(user)
            return Response({"token": str(token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(CustomUser, username=serializer.validated_data["username"])
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Подтверждение регистрации на YAMDB',
            f'Код подтверждения: {confirmation_code}',
            from_email=FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False,
            methods=['get', 'patch'],
            url_path='me',
            permission_classes=[IsAuthenticated],
            serializer_class=UserEditSerializer,
            )
    def my_profile(self, request):
        user = self.request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)