#Rengganis
from fastapi import APIRouter, HTTPException
from typing import List
from service.notif_service import get_barang_menipis, get_semua_barang_menipis
from service.stock_service import (
    get_all_barang,
    get_barang_by_id,
    tambah_barang as service_tambah,
    edit_barang,
    hapus_barang
)
from schemas.barang_schema import Barang
from schemas.response import ResponseModel
from config import THRESHOLD_MINIMUM_STOK


router = APIRouter(prefix="/stok/stok", tags=["Stok Barang"])


@router.get("/", response_model=ResponseModel[List[Barang]], summary="Tampilkan semua barang")
def tampilkan_semua_barang():
    data = get_all_barang()
    # pastikan list of Barang
    return ResponseModel[List[Barang]](
        status="success",
        message="Berhasil menampilkan semua barang",
        data=[Barang(**b) if isinstance(b, dict) else b for kategori in data.values() for b in kategori]
    )


@router.get("/barang/{id}", response_model=ResponseModel[Barang], summary="Tampilkan barang berdasarkan ID")
def ambil_barang_berdasarkan_id(id: str):
    barang = get_barang_by_id(id)
    return ResponseModel[Barang](
        status="success",
        message=f"Barang dengan ID {id} ditemukan",
        data=barang
    )


@router.post("/", response_model=ResponseModel[Barang], summary="Tambah barang")
def tambah_barang_endpoint(barang: Barang, kategori: str):
    try:
        hasil = service_tambah(barang.dict(), kategori)
        if "error" in hasil:
            raise HTTPException(status_code=400, detail=hasil["error"])
        return ResponseModel[Barang](
            status="success",
            message=hasil["message"],
            data=Barang(**hasil["data"])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding item: {str(e)}")


@router.put("/{id_barang}", response_model=ResponseModel[Barang], summary="Edit barang")
async def ubah_barang(id_barang: str, barang: Barang):
    try:
        if id_barang != barang.id:
            raise HTTPException(
                status_code=400,
                detail="ID di URL tidak sesuai dengan ID di body request"
            )
        update_data = barang.dict(exclude_unset=True)
        update_data.pop("id", None)
        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="Tidak ada data yang diberikan untuk diperbarui"
            )
        hasil = edit_barang(id_barang, update_data)
        if "error" in hasil:
            raise HTTPException(status_code=404, detail=hasil["error"])


        return ResponseModel[Barang](
            status="success",
            message=hasil["message"],
            data=Barang(**hasil["barang"])
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Terjadi kesalahan server: {str(e)}"
        )


@router.delete("/{id_barang}", summary="Hapus barang", response_model=ResponseModel[dict])
def delete_barang(id_barang: str):
    hasil = hapus_barang(id_barang)
    if "error" in hasil:
        raise HTTPException(status_code=404, detail=hasil["error"])
    return ResponseModel[dict](
        status="success",
        message=hasil["message"],
        data={"id": id_barang}
    )

