import logging
import sqlite3
from logging import info, warning

from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("Load Sqlite Logger")


class SQLiteLoader(str):

    def load_movies(self, sqlite_conn: str):

        def load_from_table(table_name, fields, conn: str, entry_count):

            table = []

            sql = "select {} from {}".format(', '.join(fields), table_name)

            def dict_factory(cur, row_factory):
                d = {}
                for idx, col in enumerate(cur.description):
                    d[col[0]] = row_factory[idx]
                return d

            conn.row_factory = dict_factory

            try:
                cursor = conn.cursor()
            except sqlite3.Error as e:
                warning('SQlite connection error')
                logging.exception(e)

            try:
                cursor.execute(sql)
                info('Read from SQlite table')
            except sqlite3.Error as e:
                warning('Read from SQlite table error')
                warning(e)

            def dbIter(cursor, sql, entry_count):
                cursor.execute(sql)
                while True:
                    results = cursor.fetchmany(entry_count)
                    if not results:
                        break
                    for result in results:
                        yield result

            records = dbIter(cursor, sql, entry_count)

            for row in records:
                table.append(row)
            cursor.close()
            return table

        film_work = []
        fields_film_work = 'id', 'title', 'description', 'creation_date', 'rating', 'type', 'created_at', 'updated_at'
        for row in load_from_table('film_work', fields_film_work, sqlite_conn, 100):
            film_work.append(
                FilmWork(row['id'], row['title'], row['description'], row['creation_date'], row['rating'], row['type'],
                         row['created_at'], row['updated_at']))

        genre = []
        fields_genre = 'id', 'name', 'description', 'created_at', 'updated_at'
        for row in load_from_table('genre', fields_genre, sqlite_conn, 100):
            genre.append(Genre(row['id'], row['name'], row['description'], row['created_at'], row['updated_at']))

        person = []
        fields_person = 'id', 'full_name', 'created_at', 'updated_at'
        for row in load_from_table('person', fields_person, sqlite_conn, 100):
            person.append(Person(row['id'], row['full_name'], row['created_at'], row['updated_at']))

        genre_film_work = []
        fields_genre_film_work = 'id', 'genre_id', 'film_work_id', 'created_at'
        for row in load_from_table('genre_film_work', fields_genre_film_work, sqlite_conn, 100):
            genre_film_work.append(GenreFilmWork(row['id'], row['genre_id'], row['film_work_id'], row['created_at']))

        person_film_work = []
        fields_person_film_work = 'id', 'person_id', 'film_work_id', 'role', 'created_at'
        for row in load_from_table('person_film_work', fields_person_film_work, sqlite_conn, 100):
            person_film_work.append(
                PersonFilmWork(row['id'], row['person_id'], row['film_work_id'], row['role'], row['created_at']))

        data = {
            'film_work': [film_work],
            'genre': [genre],
            'person': [person],
            'genre_film_work': [genre_film_work],
            'person_film_work': [person_film_work]
        }

        return data
