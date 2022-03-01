import datetime
import uuid
from dataclasses import dataclass


@dataclass
class FilmWork(object):
    __slots__ = (
        'id',
        'title',
        'description',
        'creation_date',
        'rating',
        'type',
        'created',
        'modified',
    )
    id: uuid.uuid4()
    title: str
    description: str
    creation_date: datetime.date
    rating: float
    type: str
    created: datetime.datetime
    modified: datetime.datetime


@dataclass
class Genre(object):
    __slots__ = (
        'id',
        'name',
        'description',
        'created',
        'modified',
    )
    id: uuid.uuid4()
    name: str
    description: str
    created: datetime.datetime
    modified: datetime.datetime


@dataclass
class GenreFilmWork(object):
    __slots__ = (
        'id',
        'genre_id',
        'film_work_id',
        'created',
    )
    id: uuid.uuid4()
    genre_id: uuid.uuid4()
    film_work_id: uuid.uuid4()
    created: datetime.datetime


@dataclass
class Person(object):
    __slots__ = (
        'id',
        'full_name',
        'created',
        'modified',
    )
    id: uuid.uuid4()
    full_name: str
    created: datetime.datetime
    modified: datetime.datetime


@dataclass
class PersonFilmWork(object):
    __slots__ = (
        'id',
        'person_id',
        'film_work_id',
        'role',
        'created',
    )
    id: uuid.uuid4()
    person_id: uuid.uuid4()
    film_work_id: uuid.uuid4()
    role: str
    created: datetime.datetime
