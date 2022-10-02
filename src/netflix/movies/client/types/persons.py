from uuid import UUID

from netflix.movies.client.types.common import BaseIdOrjsonSchema


class PersonShortDetail(BaseIdOrjsonSchema):
    """Person (without roles)."""

    full_name: str
    films_ids: list[UUID]


class PersonList(BaseIdOrjsonSchema):
    """List of persons."""

    full_name: str
