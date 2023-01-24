from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    email = models.EmailField('Электронная почта', unique=True, max_length=254)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль', max_length=25, choices=ROLES, default=USER)

    class Meta:
        ordering = ('pk',)

    def clean(self):
        if self.username.lower() == 'me':
            raise ValidationError(
                {'username': 'username не может быть `me`!'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
