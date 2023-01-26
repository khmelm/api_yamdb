import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class Command(BaseCommand):
    help = 'Импорт данных из csv файла.'
    success = True

    @classmethod
    def get_import_functions(cls):
        return (
            ('./api_yamdb/static/data/users.csv', cls.import_users),
            ('./api_yamdb/static/data/category.csv', cls.import_categories),
            ('./api_yamdb/static/data/genre.csv', cls.import_genres),
            ('./api_yamdb/static/data/titles.csv', cls.import_titles),
            (
                './api_yamdb/static/data/genre_title.csv',
                cls.import_titles_genres,
            ),
            ('./api_yamdb/static/data/review.csv', cls.import_reviews),
            ('./api_yamdb/static/data/comments.csv', cls.import_comments),
        )

    def handle(self, *args, **options):
        self.check_database()
        for csv_path, import_function in self.get_import_functions():
            self.import_data(csv_path, import_function)
        if self.success:
            self.stdout.write(
                self.style.SUCCESS('Записи успешно импортированы.')
            )
        else:
            self.stdout.write(
                self.style.ERROR('При импорте возникли ошибки!')
            )

    def check_database(self):
        if any([
            User.objects.count(),
            Category.objects.count(),
            Genre.objects.count(),
            Title.objects.count(),
            Review.objects.count(),
            Comment.objects.count(),
        ]):
            raise CommandError('Импорт возможен только в пустую базу данных!')

    @staticmethod
    def import_categories(row) -> None:
        Category.objects.create(**row)

    @staticmethod
    def import_genres(row) -> None:
        Genre.objects.create(**row)

    @staticmethod
    def import_users(row) -> None:
        User.objects.create_user(**row)

    @staticmethod
    def import_titles(row):
        category = Category.objects.get(pk=row.pop('category'))
        Title.objects.create(**row, category=category)

    @staticmethod
    def import_titles_genres(row):
        title = Title.objects.get(pk=row.pop('title_id'))
        genre = Genre.objects.get(pk=row.pop('genre_id'))
        title.genre.add(genre)

    @staticmethod
    def import_reviews(row):
        title = Title.objects.get(pk=row.pop('title_id'))
        author = User.objects.get(pk=row.pop('author'))
        Review.objects.create(**row, title=title, author=author)

    @staticmethod
    def import_comments(row):
        review = Review.objects.get(pk=row.pop('review_id'))
        author = User.objects.get(pk=row.pop('author'))
        Comment.objects.create(**row, review=review, author=author)

    def import_data(self, csv_path, import_function):
        with open(csv_path, newline='') as csvfile:
            for row in csv.DictReader(csvfile, delimiter=',', quotechar='"'):
                try:
                    import_function(row)
                except Exception as error:
                    row_items = dict(row.items())
                    self.stdout.write(
                        self.style.ERROR(
                            f'При импорте данных `{row_items}` возникла '
                            f'ошибка: {error}'
                        ),
                    )
                    self.success = False
