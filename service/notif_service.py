from utils.file_manager import read_json
from typing import List, Dict

BARANG_PATH = "data/barang.json"
config_PATH = "config.py"

def get_barang_menipis(id_barang: str) -> Dict:
    # Fungsi untuk memeriksa barang dengan stok menipis
    data = read_json(BARANG_PATH)
    for kategori, daftar_barang in data.items():
        for barang in daftar_barang:
            if barang.get("id") == id_barang and barang.get("stok", 0) < 10:
                return barang
    return {}

def get_semua_barang_menipis() -> List[Dict]:
    data = read_json(BARANG_PATH)
    barang_menipis = []

    for kategori, daftar_barang in data.items():
        for barang in daftar_barang:
            if barang.get("stok", 0) < 10:
                barang_menipis.append(barang)
    
    return barang_menipis
