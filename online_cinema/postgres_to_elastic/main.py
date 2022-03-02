import logging
import os
from time import sleep
from urllib.error import HTTPError

import backoff
import psycopg2
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, ElasticsearchException
from elasticsearch.helpers.actions import bulk
from models import FilmWork
from psycopg2.extras import RealDictCursor
from utils import JsonFileStorage, State

from sql import SQL

load_dotenv(".env")

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("Load Data Logger")


@backoff.on_exception(wait_gen=backoff.expo,
                      exception=(psycopg2.Error, psycopg2.OperationalError))
def extract_ids_by_date(query: str, state_date: str) -> list:
    conn = psycopg2.connect(**dsl, cursor_factory=RealDictCursor)
    ids_by_date = []
    cursor = conn.cursor()
    cursor.execute(query, {'date': state_date, })
    for row in cursor:
        ids_by_date.append(row)
    cursor.close()
    conn.close()
    return ids_by_date


@backoff.on_exception(wait_gen=backoff.expo,
                      exception=(psycopg2.Error, psycopg2.OperationalError))
def extract_ids(query: str, ids: list) -> list:
    conn = psycopg2.connect(**dsl, cursor_factory=RealDictCursor)
    fw_ids = []
    cursor = conn.cursor()
    cursor.execute(query, {'id': (tuple([i['id'] for i in ids])), })
    for row in cursor:
        fw_ids.append(row)
    cursor.close()
    conn.close()
    return fw_ids


def extract_fimwork_ids(sql: str, state_key: str) -> list:
    ids_list = extract_ids_by_date(
        sql,
        (state.get_state(state_key) or os.environ.get('DATE_FOR_LOAD')))
    if len(ids_list) > 1:
        state.set_state(state_key,
                        ids_list.pop()['modified'].isoformat())
    return ids_list


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
def load_to_elastic(extraxted_data):
    for i in extraxted_data:
        yield {
            "_index": 'movies',
            "_id": i.id,
            "_source": i.dict()
        }


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
    state_key = {'persons_updated_date': 'persons_updated_date',
                 'genres_updated_date': 'genres_updated_date',
                 'filmworks_updated_date': 'filmworks_updated_date'}
    while True:
        s = set()
        filmwork_ids = []
        for obj in [
            *
            extract_ids(
                SQL.PERSONS_FILMWORK_ID,
                extract_fimwork_ids(
                    SQL.PERSONS_ID,
                    state_key['persons_updated_date'])),
            *
            extract_ids(
                SQL.GENRES_FILMWORK_ID,
                extract_fimwork_ids(
                    SQL.GENRES_ID,
                    state_key['genres_updated_date'])),
            *
            extract_fimwork_ids(
                SQL.FILMWORK_ID,
                state_key['filmworks_updated_date'])]:
            if obj['id'] not in s:
                s.add(obj['id'])
                filmwork_ids.append(obj)
        ex = extract_ids(SQL.FILMWORK, filmwork_ids)
        bulk(elastic, load_to_elastic(extract(ex)))
        sleep(1)
