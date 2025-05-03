from typing import Optional
from pydantic import BaseModel

class Transaksi(BaseModel):
    idTransaksi: Optional[int] = None  # Use Optional for nullable types
    barang_id: str
    tipe: str
    jumlah: int
    tanggal: str