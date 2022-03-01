import logging
import os
from time import sleep
from urllib.error import HTTPError

import backoff
import psycopg2
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, ElasticsearchException
from models import FilmWork
from psycopg2.extras import RealDictCursor
from utils import JsonFileStorage, State

load_dotenv("../config/.env")

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("Load Data Logger")


query_person = f"""SELECT DISTINCT
id,
modified
FROM content.person
WHERE modified > %(date)s
ORDER BY modified
LIMIT 100;
"""


@backoff.on_exception(wait_gen=backoff.expo,
                      exception=(psycopg2.Error, psycopg2.OperationalError))
def extract_persons(query, state_date):
    conn = psycopg2.connect(**dsl, cursor_factory=RealDictCursor)
    persons = []
    cursor = conn.cursor()
    cursor.execute(query, {'date': state_date, })
    for row in cursor:
        persons.append(row)
    cursor.close()
    conn.close()
    return persons


query_genres = f"""SELECT DISTINCT
fw.id,
fw.modified
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
WHERE pfw.person_id IN %(id)s
ORDER BY fw.modified
LIMIT 1000;
"""


@backoff.on_exception(wait_gen=backoff.expo,
                      exception=(psycopg2.Error, psycopg2.OperationalError))
def extract_genres(query, persons_id):
    conn = psycopg2.connect(**dsl, cursor_factory=RealDictCursor)
    genres = []
    cursor = conn.cursor()

    cursor.execute(query, {'id': tuple([i['id'] for i in persons_id]), })
    for row in cursor:
        genres.append(row)
    cursor.close()
    conn.close()
    return genres


query_filmwork = f"""SELECT
fw.id,
fw.rating as imdb_rating,
g.name as genre,
fw.title,
fw.description,
fw.modified,
ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'director') AS director,
ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'actor') AS actors_names,
ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'writer') AS writers_names,
JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'actor') AS actors,
JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'writer') AS writers
FROM content.film_work fw
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
WHERE fw.id in %(id)s
GROUP BY fw.id, g.name
ORDER BY fw.id;
"""


@backoff.on_exception(wait_gen=backoff.expo,
                      exception=(psycopg2.Error, psycopg2.OperationalError))
def extract_filmwork(query, genres_id):
    conn = psycopg2.connect(**dsl, cursor_factory=RealDictCursor)
    filmworks = []
    cursor = conn.cursor()
    cursor.execute(query, {'id': tuple([i['id'] for i in genres_id]), })
    for row in cursor:
        filmworks.append(row)
    cursor.close()
    conn.close()
    return filmworks


def extract(extract_data):
    data = []
    for i in extract_data:
        if i['director'] is None:
            i['director'] = []
        data.append(FilmWork(**i))
    return data


@backoff.on_exception(wait_gen=backoff.expo,
                      exception=(ElasticsearchException,
                                 HTTPError,
                                 psycopg2.Error,
                                 psycopg2.OperationalError),
                      max_tries=10,
                      )
def load_to_elastic(elastic, extraxted_data):
    for i in extraxted_data:
        elastic.index(
            index='movies',
            id=i.id,
            body=i.dict()
        )


if __name__ == "__main__":
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT'),
    }
    elastic = Elasticsearch([os.environ.get("ELASTICS_HOST")])
    state = State(storage=JsonFileStorage(file_path="state.json"))
    state_key = 'updated'
    while True:
        ps = extract_persons(
            query_person,
            (state.get_state(state_key) or os.environ.get('DATE_FOR_LOAD')))
        state.set_state(state_key, ps.pop()['modified'].isoformat())
        pg = extract_genres(query_genres, ps)
        ex = extract_filmwork(query_filmwork, pg)
        load_to_elastic(elastic, extract(ex))
        sleep(1)
