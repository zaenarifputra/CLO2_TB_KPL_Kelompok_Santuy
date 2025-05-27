from collections import Counter
from typing import List, Dict, TypeVar

from utils.file_manager import read_json

T = TypeVar('T')


def tampilkan_barang_terlaris(
    data_path: str,
    id_key: str,
    jumlah_key: str,
    top_n: int = 3
) -> List[Dict[str, T]]:
    data = read_json(data_path)
    counter = Counter()

    for item in data:
        item_id = item.get(id_key)
        jumlah = item.get(jumlah_key, 0)
        if item_id is not None:
            counter[item_id] += jumlah

    return [
        {"id": item_id, "jumlah": jumlah}
        for item_id, jumlah in counter.most_common(top_n)
    ]

