from pydantic import BaseModel
class Barang(BaseModel):
    id: str
    nama: str
    berat: str
    harga: int
    stok: int