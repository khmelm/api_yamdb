from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(year):
    if year > timezone.now().year:
        raise ValidationError({
            'year': 'Год выпуска не может быть больше текущего года!'}
        )
