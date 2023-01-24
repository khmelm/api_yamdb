from django.contrib.auth import get_user_model
from django.db import models

from reviews.validators import validate_year

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('pk',)
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('pk',)
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(validators=[validate_year])
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='title',
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='title'
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='review'
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review'
    )
    score = models.IntegerField(
        'Рейтинг'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        unique_together = ('title', 'author')


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comment'
    )
    text = models.TextField('Комментарий')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comment'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
