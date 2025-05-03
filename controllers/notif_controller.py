from fastapi import APIRouter
from service.notif_service import get_barang_menipis
from service.notif_service import get_semua_barang_menipis

router = APIRouter(prefix="/stok")

@router.get("/", summary="Notifikasi semua barang dengan stok menipis")
def notif_stok_menipis():
    hasil = get_semua_barang_menipis()
    if not hasil:
        return {"message": "Semua stok dalam keadaan aman"}
    return {"stok_menipis": hasil}