import re

def validasi_stok(stok: int) -> bool:
    return stok >= 0

def valid_id_barang(id_barang: str) -> bool:
    return bool(re.fullmatch(r"[A-Z]{1,2}\d{2,5}", id_barang))

