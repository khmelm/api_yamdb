from django.utils import timezone

from django.core.exceptions import ValidationError

def validate_year(year):
    if year > timezone.now().year:
        raise ValidationError({ 
            'year': 'Год выпуска не может быть больше текущего года!'
})
