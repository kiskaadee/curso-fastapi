from typing import Generic, List, TypeVar

from pydantic import BaseModel

T = TypeVar("T")  # define a generic Type variable


class Envelope(BaseModel, Generic[T]):
    data: List[T]
    total_count: int
