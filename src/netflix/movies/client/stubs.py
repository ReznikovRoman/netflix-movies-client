import datetime
import uuid

from netflix.movies.client.clients import MovieClient
from netflix.movies.client.types import (
    FilmDetail, FilmList, PersonFullDetail, PersonList, PersonShortDetail, QueryOptions,
)
from netflix.movies.client.types.films import FilmAccessType, FilmAgeRating
from netflix.movies.client.types.roles import PersonRoleFilmList, Role

PERSON_ID = uuid.UUID("fb6a644b-436a-4131-8fbc-00ca73e9aee7")
PERSON_NAME = "Quentin Tarantino"

PERSON_SEARCH_RESULTS = [
    PersonList(uuid=PERSON_ID, full_name=PERSON_NAME),
]

FILM = FilmDetail(
    uuid=uuid.UUID("09445a09-bfb6-4eb1-84e8-c82b4fe80437"),
    title="Pulp fiction",
    imdb_rating=8.9,
    description=(
        "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits "
        "intertwine in four tales of violence and redemption."
    ),
    release_date=datetime.date(1994, 10, 14),
    age_rating=FilmAgeRating.GENERAL,
    access_type=FilmAccessType.PUBLIC,
    genre=[], actors=[], writers=[], directors=PERSON_SEARCH_RESULTS,
)

ANOTHER_FILM = FilmDetail(
    uuid=uuid.UUID("7e64ae94-4be9-4eaf-8f10-917e6ab2088c"),
    title="Kill Bill: Vol. 1",
    imdb_rating=8.2,
    description=(
        "After awakening from a four-year coma, a former assassin wreaks vengeance on the team of "
        "assassins who betrayed her."
    ),
    release_date=datetime.date(2003, 10, 10),
    age_rating=FilmAgeRating.GENERAL,
    access_type=FilmAccessType.PUBLIC,
    genre=[], actors=[], writers=[], directors=PERSON_SEARCH_RESULTS,
)

FILM_SEARCH_RESULTS = [
    FilmList(
        uuid=FILM.uuid,
        title=FILM.title,
        imdb_rating=FILM.imdb_rating,
        access_type=FILM.access_type,
    ),
    FilmList(
        uuid=ANOTHER_FILM.uuid,
        title=ANOTHER_FILM.title,
        imdb_rating=ANOTHER_FILM.imdb_rating,
        access_type=ANOTHER_FILM.access_type,
    ),
]

PERSON_SHORT_DETAILS = PersonShortDetail(
    uuid=PERSON_ID,
    full_name=PERSON_NAME,
    films_ids=[film.uuid for film in FILM_SEARCH_RESULTS],
)

PERSON_FULL_DETAILS = PersonFullDetail(
    uuid=PERSON_SHORT_DETAILS.uuid,
    full_name=PERSON_SHORT_DETAILS.full_name,
    roles=[
        PersonRoleFilmList(role=Role.DIRECTOR, films=FILM_SEARCH_RESULTS),
    ],
)


class MovieClientStub(MovieClient):
    """Netflix Movies client stub."""

    async def fetch_film_by_id(self, film_id: uuid.UUID, /) -> FilmDetail:
        return FILM

    async def find_films(
        self, query: str, /, *, fetch_all: bool = True, options: QueryOptions | None = None,
    ) -> list[FilmList]:
        return FILM_SEARCH_RESULTS

    async def find_persons(
        self, query: str, /, *, fetch_all: bool = True, options: QueryOptions | None = None,
    ) -> list[PersonList]:
        return PERSON_SEARCH_RESULTS

    async def fetch_person_short_details(self, person_id: uuid.UUID, /) -> PersonShortDetail:
        return PERSON_SHORT_DETAILS

    async def fetch_person_full_details(self, person_id: uuid.UUID, /) -> PersonFullDetail:
        return PERSON_FULL_DETAILS

    async def fetch_person_films(self, person_id: uuid.UUID, /) -> list[FilmList]:
        return FILM_SEARCH_RESULTS
