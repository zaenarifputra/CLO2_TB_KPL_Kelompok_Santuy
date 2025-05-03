from typing import Generic, TypeVar
from pydantic import BaseModel
from typing import List, TypeVar, Generic, Callable, Optional
from pydantic.generics import GenericModel

T = TypeVar ('T')

class ResponseModel(GenericModel, Generic[T]):
    status: str
    message: str
    data: T 