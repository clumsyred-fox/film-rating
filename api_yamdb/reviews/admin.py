from django.contrib import admin

from .models import Category, Comment, Genre, Title, Review, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_moderator', 'is_admin')
    list_filter = ('role',)
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'year')
    list_filter = ('category', 'year')
    search_fields = ('name', 'description')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'rating', 'pub_date')
    list_filter = ('pub_date', 'rating')
    search_fields = ('text', )
    ordering = ['-pub_date']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'pub_date')
    list_filter = ('pub_date',)
    search_fields = ('text',)

