from netflix.movies.client.types.common import BaseIdOrjsonSchema


class GenreDetail(BaseIdOrjsonSchema):
    """Genre."""

    name: str
