from fastapi import FastAPI
from controllers import (
    stock_controller,
    notif_controller,
    transaksi_controller,
    analisis_controller,
    kategori_controller
)
from service.analisis_service import tampilkan_barang_terlaris


app = FastAPI(title="StokLy - Sistem Manajemen Inventaris")

# Register routers with prefixes and tags
app.include_router(stock_controller.router, prefix="/stok", tags=["Stok Barang"])
app.include_router(notif_controller.router, prefix="/notifikasi", tags=["Notifikasi"])
app.include_router(transaksi_controller.router, prefix="/transaksi", tags=["Transaksi"])
app.include_router(analisis_controller.router, prefix="/analisis", tags=["Analisis"])
app.include_router(kategori_controller.router, prefix="/kategori", tags=["Kategori"])

# Endpoint POST untuk menambahkan produk
@app.post("/stok/")
async def add_product(product: dict):
    return {"status": "success", "data": product}

# Endpoint GET untuk mendapatkan produk berdasarkan ID
@app.get("/stok/barang/{product_id}")
async def get_product(product_id: str):
    # Simulasi mengambil produk berdasarkan ID
    return {"data": {"id": product_id, "nama": "Beras Sania", "stok": 40}}

# Endpoint PUT untuk memperbarui produk
@app.put("/stok/{product_id}")
async def update_product(product_id: str, product: dict):
    updated_product = product.copy()
    updated_product["id"] = product_id
    return {
        "status": "success",
        "message": f"Produk dengan ID {product_id} berhasil diperbarui",
        "data": updated_product
    }

# Endpoint DELETE untuk menghapus produk
@app.delete("/stok/{product_id}")
async def delete_product(product_id: str):
    # Simulasi menghapus produk berdasarkan product_id
    return {"status": "success", "message": f"Product {product_id} deleted"}

# Route untuk mendapatkan barang terlaris
# Endpoint untuk analisis (bisa ditaruh di controller, tapi ini versi langsung)
@app.get("/analisis/", tags=["Analisis"])
async def get_barang_terlaris():
    result = tampilkan_barang_terlaris(
        data_path="data/transaksi.json",  # Sesuaikan path jika perlu
        id_key="barang_id",
        jumlah_key="jumlah"
    )
    return {
        "status": "success",
        "message": "Barang terlaris berhasil ditampilkan",
        "data": result
    }
 
@app.get("/kategori/", tags=["Kategori"])
async def get_all_kategori():
    result = get_all_kategori(data_path="data/kategori.json")
    return {
        "status": "success",
        "message": "Kategori berhasil ditampilkan",
        "data": result
    } 

@app.get("/notifikasi/", tags=["Notifikasi"])
async def get_all_notifikasi():
    # Simulasi mengambil semua notifikasi
    return {
        "status": "success",
        "message": "Notifikasi berhasil ditampilkan",
        "data": [
            {"id": 1, "pesan": "Stok barang hampir habis"},
            {"id": 2, "pesan": "Transaksi berhasil"},
            {"id": 3, "pesan": "Barang baru ditambahkan"}
        ]
    }
