import logging
import os
import sqlite3

import psycopg2
from dotenv import dotenv_values, load_dotenv
from postgresql_loader import PostgresSaver
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from sqlite_loader import SQLiteLoader

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("Load Data Logger")

config = dotenv_values("../config/.env")


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres.

        Args:
              connection: connection to SQLite3
              pg_conn: connection to PostgreSQL

    @rtype: object
    @param connection: connection to SQLite3
    @param pg_conn: connection to PostgreSQL
    """
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data_from_sql = sqlite_loader.load_movies(connection)
    postgres_saver.save_all_data(data_from_sql, pg_conn)


if __name__ == '__main__':
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT'),
    }
    with sqlite3.connect(os.environ.get('SQLITE')) as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
