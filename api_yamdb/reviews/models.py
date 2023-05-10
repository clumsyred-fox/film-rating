"""Models."""

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    ROLES = [(ADMIN, "Администратор"),
             (MODERATOR, "Модератор"),
             (USER, "Пользователь")]
    bio = models.TextField("О себе", blank=True, null=True)
    role = models.CharField(
        "Роль пользователя", max_length=150, default=USER, choices=ROLES
    )
    email = models.EmailField("Почта", unique=True)
    username = models.CharField(
        "Имя пользователя", max_length=150, null=True, unique=True
    )
    confirmation_code = models.CharField(
        "Код авторизации", max_length=150, blank=True, null=True
    )

    @property
    def is_admin(self):
        """Admin."""
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        """Moder."""
        return self.role == self.MODERATOR

    class Meta:
        """Iser Meta."""

        ordering = ["id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(fields=["username", "email"],
                                    name="unique_user"),
            models.CheckConstraint(
                check=~models.Q(username__iexact="me"),
                name="username_is_not_me"
            ),
        ]

    def __str__(self):
        """User self."""
        return self.username


class BaseCategory(models.Model):
    """Базовая модель для категории и жанра"""
    name = models.CharField(max_length=256, verbose_name="Название")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Category(BaseCategory):
    """Модель категорий."""

    class Meta:
        """Category Meta."""

        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class Genre(BaseCategory):
    """Модель жанров."""

    class Meta:
        """Genre Meta."""

        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ["name"]


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    year = models.PositiveSmallIntegerField(
        verbose_name="Год выпуска",
    )
    description = models.TextField(verbose_name="Описание")
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        blank=True,
        verbose_name="Жанр",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
        verbose_name="Категория",
    )

    class Meta:
        """Meta title."""

        ordering = ["-year"]

    def __str__(self):
        """Self. title."""
        return self.name


class Review(models.Model):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField(
        "Текст",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    score = models.SmallIntegerField(
        verbose_name="Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        """Review Meta."""

        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(fields=["author", "title"],
                                    name="unique_review")
        ]

    def __str__(self):
        """Self review."""
        return self.text[:50]


class Comment(models.Model):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField("Текст")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        """Comment Meta."""

        ordering = ["pub_date"]

    def __str__(self):
        """Self comment."""
        return self.text[:50]
