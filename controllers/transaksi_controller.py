from fastapi import APIRouter
from schemas.transaksi_schema import Transaksi
from service.transaksi_service import catat_transaksi
from utils.file_manager import read_json
from schemas.response import ResponseModel
from typing import List

router = APIRouter()

@router.get("/", response_model=ResponseModel[List[Transaksi]], summary="Tampilkan semua transaksi")
def tampilkan_semua_transaksi():
    transaksi_list = read_json("data/transaksi.json")
    return ResponseModel(
        status="success",
        message="Berhasil mengambil semua transaksi",
        data=transaksi_list
    )

@router.post("/", response_model=ResponseModel[Transaksi], summary="Tambah transaksi")
def tambah_transaksi(data: Transaksi):
    result = catat_transaksi(data)
    return ResponseModel(
        status="success",
        message="Transaksi berhasil ditambahkan",
        data=result
    )
