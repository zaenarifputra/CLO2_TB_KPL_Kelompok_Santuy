from utils.file_manager import read_json
from collections import Counter

def hitung_terlaris():
    transaksi = read_json("data/transaksi.json")
    penjualan = [t["id_barang"] for t in transaksi if t["tipe"] == "keluar"]
    count = Counter(penjualan)
    return count.most_common(3)