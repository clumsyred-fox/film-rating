"""Serializers API."""

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    """User Serializer."""

    username = serializers.RegexField(
        max_length=150,
        regex=r"^[\w.@+-]",
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        """USer Meta."""

        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class SignInSerializer(serializers.ModelSerializer):
    """Sign In Serializer."""

    username = serializers.RegexField(max_length=150, regex=r"^[\w.@+-]+\Z")
    email = serializers.EmailField(
        max_length=254,
    )

    class Meta:
        """Sign In Meta."""

        model = User
        fields = ("email", "username")

    def validate(self, data):
        """Sign in valid."""
        if data.get("username") == "me":
            raise serializers.ValidationError("Поменяйте имя")
        return data


class TokenSerializer(serializers.ModelSerializer):
    """Token Serializer."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=150)

    class Meta:
        """Token Meta."""

        model = User
        fields = ("username", "confirmation_code")


class CategorySerializer(serializers.ModelSerializer):
    """Category Serializer."""

    lookup_field = "slug"

    class Meta:
        """Category Meta."""

        model = Category
        fields = (
            "name",
            "slug",
        )


class GenreSerializer(serializers.ModelSerializer):
    """Genre Serializer."""

    lookup_field = "slug"

    class Meta:
        """Genre Meta."""

        model = Genre
        fields = (
            "name",
            "slug",
        )


class CategoryTitle(serializers.SlugRelatedField):
    """CategoryTitle Serializer."""

    def to_representation(self, value):
        """For using."""
        serializer = CategorySerializer(value)
        return serializer.data


class GenreTitle(serializers.SlugRelatedField):
    """GenreTitle Serializer."""

    def to_representation(self, value):
        """For using."""
        serializer = GenreSerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    """Title Serializer."""

    category = CategoryTitle(
        slug_field="slug", queryset=Category.objects.all(), required=False
    )
    genre = GenreTitle(slug_field="slug",
                       queryset=Genre.objects.all(), many=True)
    rating = serializers.IntegerField(source="reviews__score__avg",
                                      read_only=True)

    class Meta:
        """Title Meta."""

        model = Title
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """Review Serializer."""

    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        """Review Meta."""

        fields = "__all__"
        model = Review
        read_only_fields = ("title",)

    def validate(self, data):
        """Review valid."""
        title_id = self.context["view"].kwargs.get("title_id")
        author = self.context.get("request").user
        title = get_object_or_404(Title, pk=title_id)
        if (
            title.reviews.filter(author=author).exists()
            and self.context.get("request").method != "PATCH"
        ):
            raise serializers.ValidationError("Уже есть ваш отзыв!")
        return data

    def validate_score(self, value):
        """Score valid."""
        if value < 1 or value > 10:
            raise serializers.ValidationError("Недопустимое значение!")
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Comment Serializer."""

    author = SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        """Comment Meta."""

        fields = "__all__"
        model = Comment
        read_only_fields = ("review",)
