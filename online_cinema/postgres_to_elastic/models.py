import uuid
from typing import Optional

from pydantic import BaseModel


class Person(BaseModel):
    id: uuid.UUID
    name: str


class FilmWork(BaseModel):
    id: uuid.UUID
    imdb_rating: Optional[float]
    genre: str
    title: str
    description: Optional[str]
    director: Optional[list[str]]
    actors_names: Optional[list[str]]
    writers_names: Optional[list[str]]
    actors: Optional[list[Person]]
    writers: Optional[list[Person]]
