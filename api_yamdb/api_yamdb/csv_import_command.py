import pandas as pd
import sqlite3

file_list = ['api_yamdb/static/data/category.csv',
             'api_yamdb/static/data/comments.csv',
             'api_yamdb/static/data/genre_title.csv',
             'api_yamdb/static/data/genre.csv',
             'api_yamdb/static/data/review.csv',
             'api_yamdb/static/data/titles.csv',
             'api_yamdb/static/data/users.csv']

db_path = 'api_yamdb/db.sqlite3'


def insert_csvs_into_sqlite(file_list, db_path):
    conn = sqlite3.connect(db_path)

    for file_path in file_list:
        df = pd.read_csv(file_path)
        table_name = file_path.split("/")[-1].split(".")[0]
        df.to_sql(table_name, conn, if_exists='replace')

    conn.close()


insert_csvs_into_sqlite(file_list, db_path)
