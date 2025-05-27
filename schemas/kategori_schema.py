# shafiq
from pydantic import BaseModel, Field

class Kategori(BaseModel):
    id_kategori: str = Field(..., alias="idKategori", example="KTG001", description="ID unik kategori")
    nama: str = Field(..., example="Makanan", description="Nama kategori")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "idKategori": "KTG001",
                "nama": "Makanan"
            }
        }
