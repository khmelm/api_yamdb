## Учебный проект "YaMDb"

### Описание проекта:

Проект *YaMDb* позволяет пользователям оставлять отзывы на произведения.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».
Список категорий может быть расширен.
Произведению может быть присвоен жанр из списка предустановленных.
Пользователь может оставить отзыв на произведение (в виде текста и оценки).
Пользователи могут оставлять комментарии к отзывам.

Наш сервис позволяет:

* Создавать учётные записи
* Работать с учётными записями пользователей (получение, изменение данных, удаление аккаунта)
* Получать список всех категорий, жанров, произведений, отзывов, комментариев
* Добавлять, редактировать, удалять категорию, жанр, произведение, отзыв, комментарий

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:khmelm/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры работы сервиса:

```
Запрос: POST http://localhost:8000/api/v1/auth/signup/
{
  "email": "user@example.com",
  "username": "string"
}

Результат:
{
  "email": "string",
  "username": "string"
}
```

```
Запрос: GET http://localhost:8000/api/v1/titles/

Результат:
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```

```
Запрос: GET http://localhost:8000/api/v1/titles/{title_id}/reviews/

Результат:
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
