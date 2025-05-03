from fastapi import FastAPI
from controllers import (
    stock_controller,
    notif_controller,
    transaksi_controller,
    analisis_controller,
    kategori_controller
)

app = FastAPI(title="StokLy - Sistem Manajemen Inventaris")

# Register routers with prefixes and tags
app.include_router(stock_controller.router, prefix="/stok", tags=["Stok Barang"])
app.include_router(notif_controller.router, prefix="/notifikasi", tags=["Notifikasi"])
app.include_router(transaksi_controller.router, prefix="/transaksi", tags=["Transaksi"])
app.include_router(analisis_controller.router, prefix="/analisis", tags=["Analisis"])
app.include_router(kategori_controller.router, prefix="/kategori", tags=["Kategori"])
