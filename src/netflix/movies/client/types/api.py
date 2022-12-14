from dataclasses import dataclass, field
from typing import Any

from netflix.movies.client.constants import DEFAULT_PAGE_NUMBER, DEFAULT_PAGE_SIZE

dataclass_options = {
    "init": True,
    "repr": True,
    "eq": True,
    "order": True,
    "unsafe_hash": True,
    "frozen": True,
    "kw_only": True,
    "match_args": True,
    "slots": True,
}


@dataclass(**dataclass_options)
class SortOptions:
    """Sort options."""

    sort: list[str] = field(default_factory=list)


@dataclass(**dataclass_options)
class PageNumberPaginationOptions:
    """`Page number` pagination options."""

    page_number: int = DEFAULT_PAGE_NUMBER
    page_size: int = DEFAULT_PAGE_SIZE


@dataclass(**dataclass_options)
class QueryOptions:
    """Query options."""

    sort: SortOptions = field(default_factory=SortOptions)
    page_number_pagination: PageNumberPaginationOptions = field(default_factory=PageNumberPaginationOptions)

    def to_dict(self) -> dict[str, Any]:
        dct = {
            "sort": self.sort.sort,
            "page[number]": self.page_number_pagination.page_number,
            "page[size]": self.page_number_pagination.page_size,
        }
        return dct
