# shafiq
from fastapi import APIRouter
from schemas.response import ResponseModel
from service.kategori_service import get_all_kategori
from typing import List, Dict


router = APIRouter()


@router.get("/", response_model=ResponseModel[List[Dict]], summary="Tampilkan semua kategori")
def tampilkan_semua_kategori():
    result = get_all_kategori(data_path="data/kategori.json")
    return ResponseModel(
        status="success",
        message="Kategori berhasil ditampilkan",
        data=result
    )
