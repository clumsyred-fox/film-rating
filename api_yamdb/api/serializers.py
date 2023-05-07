from rest_framework import serializers
import re
from rest_framework.relations import SlugRelatedField
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator

from reviews.models import User, Category, Title, Genre,  Review, Comment


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(max_length = 150,
                                      regex=r'^[\w.@+-]',
                                      validators=[UniqueValidator(queryset=User.objects.all())]
                                      )
    email = serializers.EmailField(max_length = 254,
                                   validators=[UniqueValidator(queryset=User.objects.all())]
                                   )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class SignInSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        max_length = 150,
        regex=r'^[\w.@+-]+\Z')
    email = serializers.EmailField(
        max_length = 254,)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('Поменяйте имя')
        return data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):
    lookup_field = 'slug'

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class CategoryTitle(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class GenreTitle(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryTitle(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )
    genre = GenreTitle(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context.get('request').user
        title = get_object_or_404(Title, id=title_id)
        if (title.reviews.filter(author=author).exists()
           and self.context.get('request').method != 'PATCH'):
            raise serializers.ValidationError(
                'Можно оставлять только один отзыв!'
            )
        return data

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Недопустимое значение!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)
