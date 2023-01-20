import datetime

from django.core.exceptions import ValidationError

def validate_year(year):
    if year > datetime.datetime.now().year:
        raise ValidationError(
                {'Год выпуска не может быть больше текущего года!'})
    