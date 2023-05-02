"""Import files."""

import csv

from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Comment, Genre, Review, Title, User

CSV_PATH = 'static/data/'

FOREIGN_KEY_FIELDS = ('category', 'author')

DICT = {
    User: 'users.csv',
    Genre: 'genre.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv'
}


def csv_serializer(csv_data, model):
    """CSV load."""
    objs = []
    for row in csv_data:
        for field in FOREIGN_KEY_FIELDS:
            if field in row:
                row[f'{field}_id'] = row[field]
                del row[field]
        objs.append(model(**row))
    model.objects.bulk_create(objs)


class Command(BaseCommand):
    """Класс выполнения."""

    help = 'Load data from csv file into the database'

    def handle(self, *args, **kwargs):
        """Load files."""
        for model, file_name in DICT.items():
            try:
                with open(CSV_PATH + file_name,
                          newline='', encoding='utf8') as csv_file:
                    csv_data = csv.DictReader(csv_file)
                    csv_serializer(csv_data, model)
            except Exception as e:
                raise CommandError(e)
            print('Данные успешно заргружены.')
