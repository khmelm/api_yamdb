from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


class BaseNameSlugAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('text',)


@admin.register(Category)
class PostAdmin(BaseNameSlugAdmin):
    pass


@admin.register(Genre)
class PostAdmin(BaseNameSlugAdmin):
    pass


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'description', 'category')
    search_fields = ('name', 'description')
    list_filter = ('year', 'category', 'genre')


@admin.register(Review)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('title', 'text')
    list_filter = ('score', 'pub_date')


@admin.register(Comment)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)
