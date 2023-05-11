"""API views."""

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User

from api.filters import TitlesFilter
from api.permissions import Admin, AdminModerAuthorReadOnly, AdminReadOnly
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignInSerializer,
    TitleSerializer,
    TokenSerializer,
    UserSerializer,
)


class GetPostDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Custom mixin."""


class SignInView(APIView):
    """Register view."""

    def post(self, request):
        """Registration."""
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user, _ = User.objects.get_or_create(
                    username=serializer.validated_data["username"],
                    email=serializer.validated_data["email"],
                )
            except IntegrityError:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                settings.MAIL_SUBJECT,
                confirmation_code,
                settings.FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    """Obtain Token."""

    def post(self, request):
        """Get token."""
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data["username"]
            confirmation_code = serializer.data["confirmation_code"]
            user = get_object_or_404(User, username=username)
            if confirmation_code != user.confirmation_code:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken.for_user(user)
            return Response(
                {"token": str(token.access_token)}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """View user(s)."""

    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [Admin]
    http_method_names = ["get", "post", "head", "patch", "delete"]

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        url_path="me",
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserSerializer,
    )
    def own_profile(self, request):
        """See youself."""
        user = self.request.user
        if request.method == "GET":
            serializer = UserSerializer(user)
            return Response(serializer.data)
        elif request.method == "PATCH":
            serializer = self.get_serializer(user,
                                             data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data["role"] = request.user.role
            serializer.save()
            return Response(serializer.data)


class CategoryViewSet(GetPostDeleteViewSet):
    """View category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminReadOnly]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ["name"]
    lookup_field = "slug"


class GenreViewSet(GetPostDeleteViewSet):
    """View genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminReadOnly]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    """View title."""

    queryset = Title.objects.all().annotate(
        Avg("reviews__score")).order_by("name")
    permission_classes = [AdminReadOnly]
    serializer_class = TitleSerializer
    filterset_class = TitlesFilter


class ReviewViewSet(viewsets.ModelViewSet):
    """View review."""

    serializer_class = ReviewSerializer
    permission_classes = [AdminModerAuthorReadOnly]

    def get_queryset(self):
        """GET review."""
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        """CREATE review."""
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """View comment."""

    serializer_class = CommentSerializer
    permission_classes = [AdminModerAuthorReadOnly]

    def get_queryset(self):
        """GET comment."""
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        """CREATE comment."""
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)
