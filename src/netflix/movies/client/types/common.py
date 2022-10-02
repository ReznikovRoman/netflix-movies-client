import uuid
from typing import TypeAlias

from orjson import orjson
from pydantic import BaseModel

Id: TypeAlias = int

TimeoutScalarType: TypeAlias = int | float
TimeoutTupleType: TypeAlias = tuple[TimeoutScalarType, TimeoutScalarType]
TimeoutType: TypeAlias = TimeoutScalarType | TimeoutTupleType


def orjson_dumps(value, *, default):
    return orjson.dumps(value, default=default).decode()


class BaseOrjsonSchema(BaseModel):
    """Base Pydantic `orjson` schema."""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class BaseIdOrjsonSchema(BaseOrjsonSchema):
    """Base schema with uuid."""

    uuid: uuid.UUID
