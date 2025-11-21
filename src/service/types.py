from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')

class Paginated(BaseModel, Generic[T]):
    items: List[T]
    total_items: int
    total_pages: int

    model_config = {
        "arbitrary_types_allowed": True
    }
