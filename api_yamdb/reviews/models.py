from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

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
        verbose_name='Никнейм',
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
    name = models.CharField(max_length=256)
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
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
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
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        verbose_name='Категория произведения',
    )
    name = models.CharField(max_length=256,
                            verbose_name='Название произведения')
    year = models.IntegerField(verbose_name='Дата создания произведения')

    def clean(self):
        if self.year > int(timezone.now().year):
            raise ValidationError(
                'Ваша дата не может быть больше текущей даты.'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

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
