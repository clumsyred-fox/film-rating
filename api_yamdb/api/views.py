from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings 
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, User, Review, Title
from .filters import TitlesFilter
from .permissions import (AdminReadOnly,
                          Admin,
                          AdminModerAuthorReadOnly)
from .serializers import (TokenSerializer,
                          SignInSerializer,
                          UserSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          ReviewSerializer,
                          CommentSerializer)


class GetPostDeleteViewSet(mixins.CreateModelMixin, 
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin, 
                           viewsets.GenericViewSet):
    pass


class SignInView(APIView):
    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            user, _ = User.objects.get_or_create(username=serializer.validated_data['username'] ,
                                                 email=serializer.validated_data['email'])
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                settings.MAIL_SUBJECT,
                confirmation_code,
                settings.FROM_EMAIL,
                [user.email],
                fail_silently=False)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            confirmation_code = serializer.data['confirmation_code']
            user = get_object_or_404(User, username=username)
            if confirmation_code != user.confirmation_code:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken.for_user(user)
            return Response({'token': str(token.access_token)},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [Admin]
    
    @action(
        methods=["GET", "PATCH"],
        detail=False,
        url_path="me",
        permission_classes=[permissions.IsAuthenticated])
    def own_profile(self, request):
        serializer = UserSerializer(request.user)
        if request.method == "PATCH":
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True)
            if serializer.is_valid():
                serializer.validated_data['role'] = request.user.role
                serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(GetPostDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminReadOnly]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ["name"]
    lookup_field = "slug"


class GenreViewSet(GetPostDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminReadOnly]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')).order_by('name')

    permission_classes = [AdminReadOnly]
    serializer_class = TitleSerializer
    filterset_class = TitlesFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AdminModerAuthorReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AdminModerAuthorReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
