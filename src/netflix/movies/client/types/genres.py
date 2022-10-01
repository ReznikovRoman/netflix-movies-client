from netflix.movies.client.types.common import BaseIdOrjsonSchema


class GenreDetail(BaseIdOrjsonSchema):
    """Жанр фильма."""

    name: str
