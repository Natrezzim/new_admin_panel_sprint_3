import collections
import os
import sqlite3

import psycopg2
from dotenv import dotenv_values, load_dotenv

load_dotenv()
config = dotenv_values("../../config/.env")

sqlite_conn = sqlite3.connect(os.environ.get('SQLITE'))

pg_conn = psycopg2.connect(dbname=os.environ.get('DB_NAME'), user=os.environ.get('DB_USER'),
                           password=os.environ.get('DB_PASSWORD'), host=os.environ.get('DB_HOST'), port=os.environ.get('DB_PORT'))

cursor_sqlite = sqlite_conn.cursor()
cursor_postgresql = pg_conn.cursor()


def test_film_work_row_count():
    count_of_rows_sqlite = cursor_sqlite.execute('select count(*) from film_work').fetchall()
    cursor_postgresql.execute('select count(*) from content.film_work')
    counts_of_rows_postgresql = cursor_postgresql.fetchall()
    assert counts_of_rows_postgresql == count_of_rows_sqlite


def test_genre_row_count():
    count_of_rows_sqlite = cursor_sqlite.execute('select count(*) from genre').fetchall()
    cursor_postgresql.execute('select count(*) from content.genre')
    counts_of_rows_postgresql = cursor_postgresql.fetchall()
    assert counts_of_rows_postgresql == count_of_rows_sqlite


def test_genre_film_work_row_count():
    count_of_rows_sqlite = cursor_sqlite.execute('select count(*) from genre_film_work').fetchall()
    cursor_postgresql.execute('select count(*) from content.genre_film_work')
    counts_of_rows_postgresql = cursor_postgresql.fetchall()
    assert counts_of_rows_postgresql == count_of_rows_sqlite


def test_person_row_count():
    count_of_rows_sqlite = cursor_sqlite.execute('select count(*) from person').fetchall()
    cursor_postgresql.execute('select count(*) from content.person')
    counts_of_rows_postgresql = cursor_postgresql.fetchall()
    assert counts_of_rows_postgresql == count_of_rows_sqlite


def test_person_film_work_row_count():
    count_of_rows_sqlite = cursor_sqlite.execute('select count(*) from person_film_work').fetchall()
    cursor_postgresql.execute('select count(*) from content.person_film_work')
    counts_of_rows_postgresql = cursor_postgresql.fetchall()
    assert counts_of_rows_postgresql == count_of_rows_sqlite


def test_film_work_data():
    cursor_sqlite.execute(
        'select id, title, description, creation_date, rating, type from film_work')
    sqlite_result = cursor_sqlite.fetchall()
    cursor_postgresql.execute(
        'select id, title, description, creation_date, rating, type from content.film_work')
    postgreslq_result = cursor_postgresql.fetchall()
    assert collections.Counter(postgreslq_result) == collections.Counter(sqlite_result)


def test_genre_data():
    cursor_sqlite.execute(
        'select id, name, description from genre')
    sqlite_result = cursor_sqlite.fetchall()
    cursor_postgresql.execute(
        'select id, name, description from content.genre')
    postgreslq_result = cursor_postgresql.fetchall()
    assert collections.Counter(postgreslq_result) == collections.Counter(sqlite_result)


def test_genre_film_work_data():
    cursor_sqlite.execute(
        'select id, genre_id, film_work_id from genre_film_work')
    sqlite_result = cursor_sqlite.fetchall()
    cursor_postgresql.execute(
        'select id, genre_id, film_work_id from content.genre_film_work')
    postgreslq_result = cursor_postgresql.fetchall()
    assert collections.Counter(postgreslq_result) == collections.Counter(sqlite_result)


def test_person_film_work_data():
    cursor_sqlite.execute(
        'select id, person_id, film_work_id, role from person_film_work')
    sqlite_result = cursor_sqlite.fetchall()
    cursor_postgresql.execute(
        'select id, person_id, film_work_id, role from content.person_film_work')
    postgreslq_result = cursor_postgresql.fetchall()
    assert collections.Counter(postgreslq_result) == collections.Counter(sqlite_result)


def test_person_data():
    cursor_sqlite.execute(
        'select id, full_name from person')
    sqlite_result = cursor_sqlite.fetchall()
    cursor_postgresql.execute(
        'select id, full_name from content.person')
    postgreslq_result = cursor_postgresql.fetchall()
    assert collections.Counter(postgreslq_result) == collections.Counter(sqlite_result)
