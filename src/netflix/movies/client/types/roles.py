from enum import Enum

from netflix.movies.client.types.common import BaseIdOrjsonSchema, BaseOrjsonSchema
from netflix.movies.client.types.films import FilmList


class Role(str, Enum):
    """Person's role."""

    ACTOR = "actor"
    WRITER = "writer"
    DIRECTOR = "director"


class PersonRoleFilmList(BaseOrjsonSchema):
    """Person's role with corresponding films."""

    role: Role
    films: list[FilmList]


class PersonFullDetail(BaseIdOrjsonSchema):
    """Person (with roles and films)."""

    full_name: str
    roles: list[PersonRoleFilmList]
