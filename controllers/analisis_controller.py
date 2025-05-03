from fastapi import APIRouter
from service.analisis_service import tampilkan_barang_terlaris
from schemas.response import ResponseModel
from typing import List, Dict
router = APIRouter()


@router.get("/", response_model=ResponseModel[List[Dict]], summary="Tampilkan 3 barang terlaris")
def barang_terlaris():
    result = tampilkan_barang_terlaris(
        data_path="data/transaksi.json", 
        id_key="barang_id", 
        jumlah_key="jumlah"
    )
    return ResponseModel(
        status="success",
        message="Barang terlaris berhasil ditampilkan",
        data=result
    )
