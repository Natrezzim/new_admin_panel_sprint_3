import logging
from dataclasses import asdict
from logging import info, warning

import psycopg2

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("Load Postgresql Logger")


class PostgresSaver(str):

    @staticmethod
    def save_all_data(data, pg_conn: str):

        def save_to_table(table_name: str, fields, conn: str):
            cursor = conn.cursor()
            values = []
            for i in enumerate(fields):
                i = '%s'
                values.append(i)

            sql = "insert into content.{} ({}) values ({}) on conflict do nothing".format(
                table_name, ', '.join(fields), ', '.join(values))
            data_dict = []
            for row in data.get(table_name):
                for entry in row:
                    data_dict.append(asdict(entry))

            try:
                info('Write to PostgreSQL table {}'.format(table_name))
                for i in data_dict:
                    column = i.keys()
                    values = [i[column] for column in column]
                    cursor.execute(sql, values)

            except psycopg2.Error as e:
                warning('Write to PostgreSQL film_work table error')
                logging.exception(e)

            cursor.close()

        fields_film_work = 'id', 'title', 'description', 'creation_date', 'rating', 'type', 'created', 'modified'
        save_to_table('film_work', fields_film_work, pg_conn)
        fields_genre = 'id', 'name', 'description', 'created', 'modified'
        save_to_table('genre', fields_genre, pg_conn)
        fields_person = 'id', 'full_name', 'created', 'modified'
        save_to_table('person', fields_person, pg_conn)
        fields_genre_film_work = 'id', 'genre_id', 'film_work_id', 'created'
        save_to_table('genre_film_work', fields_genre_film_work, pg_conn)
        fields_person_film_work = 'id', 'person_id', 'film_work_id', 'role', 'created'
        save_to_table('person_film_work', fields_person_film_work, pg_conn)
