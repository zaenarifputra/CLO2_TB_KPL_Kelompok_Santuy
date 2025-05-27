from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import List, Optional
from controllers import (
    stock_controller,
    notif_controller,
    transaksi_controller,
    analisis_controller,
    kategori_controller
)
from service.analisis_service import tampilkan_barang_terlaris
from service.kategori_service import get_all_kategori  
from schemas.barang_schema import Barang

app = FastAPI(title="StokLy - Sistem Manajemen Inventaris")


# ------------------ Routers ------------------

app.include_router(stock_controller.router, prefix="/stok", tags=["Stok Barang"])
app.include_router(notif_controller.router, prefix="/notifikasi", tags=["Notifikasi"])
app.include_router(transaksi_controller.router, prefix="/transaksi", tags=["Transaksi"])
app.include_router(analisis_controller.router, prefix="/analisis", tags=["Analisis"])
app.include_router(kategori_controller.router, prefix="/kategori", tags=["Kategori"])

# ------------------ Endpoints ------------------

@app.post("/stok/", tags=["Stok Barang"])
async def add_product(product: Barang):
    return {"status": "success", "data": product}

@app.get("/stok/barang/{product_id}", tags=["Stok Barang"])
async def get_product(product_id: str):
    if product_id != "BR01":
        raise HTTPException(status_code=404, detail="Product not found")
    return {"data": {"id": product_id, "nama": "Beras Sania", "stok": 40}}

@app.put("/stok/{product_id}", tags=["Stok Barang"])
async def update_product(product_id: str, product: Barang):
    if product_id != "BR06":
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product = product.dict()
    updated_product["id"] = product_id
    return {
        "status": "success",
        "message": f"Produk dengan ID {product_id} berhasil diperbarui",
        "data": updated_product
    }

@app.delete("/stok/{product_id}", tags=["Stok Barang"])
async def delete_product(product_id: str):
    if product_id != "BR06":
        raise HTTPException(status_code=404, detail="Product not found")
    return {"status": "success", "message": f"Product {product_id} deleted"}


@app.get("/analisis/", tags=["Analisis"])
async def get_barang_terlaris():
    result = tampilkan_barang_terlaris(
        data_path="data/transaksi.json",
        id_key="barang_id",
        jumlah_key="jumlah"
    )
    return {
        "status": "success",
        "message": "Barang terlaris berhasil ditampilkan",
        "data": result
    }

@app.get("/kategori/", tags=["Kategori"])
async def get_all_kategori_route():
    result = get_all_kategori(data_path="data/kategori.json")
    return {
        "status": "success",
        "message": "Kategori berhasil ditampilkan",
        "data": result
    }

@app.get("/notifikasi/", tags=["Notifikasi"])
async def get_all_notifikasi():
    return {
        "status": "success",
        "message": "Notifikasi berhasil ditampilkan",
        "data": []  
    }
