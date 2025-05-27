from collections import Counter
from utils.file_manager import read_json


def hitung_terlaris(data_path: str = "data/transaksi.json", tipe_keluar: str = "keluar", top_n: int = 3):
    transaksi = read_json(data_path)
    
    penjualan = [
        item["id_barang"]
        for item in transaksi
        if item.get("tipe") == tipe_keluar and "id_barang" in item
    ]
    
    counter = Counter(penjualan)
    
    return counter.most_common(top_n)
