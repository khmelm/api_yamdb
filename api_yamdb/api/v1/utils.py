from django.conf import settings
from django.core.mail import send_mail


def send_confirmation_code(code, mail):
    send_mail(
        subject='YaMDb confirmation code',
        message='Здравствуйте!\n\nВаш код подтверждения для входа на сайт '
        f'YaMDb: {code}\n\nС наилучшими пожеланиями,\nКоманда YaMDb.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[mail],
        fail_silently=False,
    )
