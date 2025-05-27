from utils.file_manager import read_json
from collections import Counter
from typing import List, Dict, TypeVar
from typing import List, Dict, Tuple


# Definisikan TypeVar yang dapat digunakan di method
T = TypeVar('T')


def tampilkan_barang_terlaris(data_path: str, id_key: str, jumlah_key: str, top_n: int = 3) -> List[Dict[str, T]]:
    data = read_json(data_path)
    counter = Counter()


    for item in data:
        item_id = item.get(id_key)
        jumlah = item.get(jumlah_key, 0)
        counter[item_id] += jumlah
    # Menggunakan generic T untuk nilai yang bisa bervariasi (seperti int atau str)
    return [{"id": item[0], "jumlah": item[1]} for item in counter.most_common(top_n)]
