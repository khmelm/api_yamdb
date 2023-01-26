from django.core.mail import send_mail


def send_confirmation_code(code, mail):
    send_mail(
        'Ваш код подтверждения для входа на сайт YaMDb',
        'Здравствуйте!\n\nВаш код подтверждения для входа на сайт YaMDb: '
        f'{code}\n\nС наилучшими пожеланиями,\nКоманда YaMDb.',
        None,
        [mail],
        fail_silently=False,
    )
