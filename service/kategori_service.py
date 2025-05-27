# shafiq
from typing import TypeVar, List
from utils.file_manager import read_json
T = TypeVar("T")

def get_all_items_from_json(data_path: str) -> List[T]:
    return read_json(data_path)