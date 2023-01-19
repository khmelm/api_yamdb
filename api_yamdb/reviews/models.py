from datetime import date

from django.db import models

from api.validators import validate_year

class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(validators=[validate_year])
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='titles',
    )

    def __str__(self):
        return self.name


