# schemas/barang_schema.py
from pydantic import BaseModel, Field

class Barang(BaseModel):
    id: str
    nama: str
    berat: str
    harga: int
    stok: int = Field(..., ge=0, description="Stok tidak boleh negatif")
