# shafiq
from utils.file_manager import read_json
from typing import TypeVar, List


T = TypeVar('T') 


def get_all_kategori(data_path: str) -> List[T]:
    return read_json(data_path)  # Ini akan mengembalikan tipe data yang ada dalam file JSON