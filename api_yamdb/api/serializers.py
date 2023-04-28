from rest_framework import serializers
from api_yamdb.reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """ Сериализатор категорий """
    class Meta:
        model = Category
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    """ Сериализатор жанров """
    class Meta:
        model = Genre
        fields = ['name', 'slug']


class TitleGETSerializer(serializers.ModelSerializer):
    """ Сериализатор вывода произведений """
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = ['name', 'year', 'genre', 'category']


class TitlePOSTSerializer(serializers.ModelSerializer):
    """ Сериализатор создания произведений """
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = ['name', 'year', 'description', 'genre', 'category']
