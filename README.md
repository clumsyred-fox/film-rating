# Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

# Установка и запуск:
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

Запустить проект:
```
python3 manage.py runserver
```

# Примеры использования
## Все примеры запросов и ответов смотрите на http://127.0.0.1:8000/redoc/ после установки и запуска проекта.