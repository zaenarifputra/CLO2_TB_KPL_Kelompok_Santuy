# shafiq
from fastapi import APIRouter
from typing import List, Dict

from schemas.response import ResponseModel
from service.kategori_service import get_all_kategori

router = APIRouter()

@router.get(
    "/",
    response_model=ResponseModel[List[Dict]],
    summary="Tampilkan semua kategori",
    tags=["Kategori"]
)
def tampilkan_semua_kategori():
    """
    Endpoint untuk menampilkan semua data kategori.

    Returns:
        ResponseModel: Objek response berisi daftar kategori.
    """
    kategori_list = get_all_kategori(data_path="data/kategori.json")
    return ResponseModel(
        status="success",
        message="Kategori berhasil ditampilkan",
        data=kategori_list
    )
