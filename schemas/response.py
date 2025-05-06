from typing import Generic, TypeVar
from pydantic import BaseModel
from typing import List, TypeVar, Generic, Callable, Optional
from pydantic import BaseModel

T = TypeVar ('T')

class ResponseModel(BaseModel, Generic[T]):
    status: str
    message: str
    data: T 