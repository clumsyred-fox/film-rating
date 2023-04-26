from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Custom User Model


class CustomUser(AbstractUser):
    CHOICES = (
        ('USER', 'User'),
        ('ADMIN', 'Admin'),
        ('MODERATOR', 'Moderator'),
    )
    username_validator = RegexValidator(
        r'^[\w.@+-]+\z',
        'Required. 150 characters or fewer.'
        'Letters, digits and @/./+/-/_ only.'
    )
    username = models.CharField(
        ('username'),
        max_length=150,
        unique=True,
        help_text=(
            'Required. 150 characters or fewer.'
            'Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator],
        error_messages={'unique': 'User with that username already exists.'},
    )
    bio = models.TextField(max_length=250, verbose_name='Биография')
    role = models.CharField(
        max_length=20,
        verbose_name='Статус пользователя',
        choices=CHOICES,
        default='USER',
    )
    email = models.EmailField(max_length=254, unique=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Only alphanumeric characters,'
                'dashes, and underscores are allowed.',
            )
        ],
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Only alphanumeric characters,'
                'dashes, and underscores are allowed.',
            )
        ],
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Titles(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория произведения',
    )
    name = models.CharField(max_length=256,
                            verbose_name='Название произведения')
    year = models.IntegerField(verbose_name='Дата создания произведения')
    description = models.TextField(
        blank=True, null=True, verbose_name='Описание произведения'
    )
    genre = models.ManyToManyField(
        Genre, blank=True, db_index=True, verbose_name='Жанр произведения'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
