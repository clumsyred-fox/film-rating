# Описание
___
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

# Разработчики:
___
* Елизавета Ганецкая ([ссылка на GitHub](https://github.com/ligany)):
Разработка моделей "Отзывы" (Review) и "Комментарии" (Comments), а также разработка представлений и эндпойнтов для них. Cистема подтверждения через e-mail. Создание системы рейтенгов.
* Сергей Лющин ([ссылка на GitHub](https://github.com/XviD1231)):
Разработка моделей: "Произведения" (Titles), "Категории" (Categories), "Жанры" (Genres), а также  представлений и эндпойнтов для них. Импорт данных из CSV-файлов.
* Андрей Пугач ([ссылка на GitHub](https://github.com/Pugaman22)):
Разработка системы регистрации и аутентификации, прав доступа, реализация токена.
# Стек технологий:
___
![Python](https://img.shields.io/badge/Python%20-3.9-blueviolet) ![Django](https://img.shields.io/badge/Django%20-3.2-blueviolet) ![DRF](https://img.shields.io/badge/DjangoRestFramework-3.12.4-blueviolet) ![simple](https://img.shields.io/badge/DjangoRestFramework--simplejwt-5.2.2-blueviolet)
# Установка и запуск:
___
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:ligany/api_yamdb.git
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
source env/bin/activate
```

Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:
```
python3 manage.py migrate
```
Загрузите тестовые данные:
```
python3 manage.py load_data
```
Запустить проект:
```
python3 manage.py runserver
```

# Примеры использования
## Все примеры запросов и ответов смотрите на http://127.0.0.1:8000/redoc/ после установки и запуска проекта.