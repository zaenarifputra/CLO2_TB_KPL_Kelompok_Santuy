from ctypes.wintypes import MAX_PATH
from fastapi import HTTPException
from schemas.barang_schema import Barang
from utils.file_manager import read_json, write_json
from utils.validator import valid_id_barang
from typing import Union
import json
import os


BARANG_PATH = "data/barang.json"


def get_all_barang() -> list:
    return read_json(BARANG_PATH)


def get_barang_by_id(id_barang: str) -> Barang:
    if not valid_id_barang(id_barang):
        raise HTTPException(
            status_code=400,
            detail="Format ID barang tidak valid. Gunakan format seperti A123 atau B0001."
        )


    data = read_json(BARANG_PATH)
    for kategori in data.values():
        for barang in kategori:
            if barang["id"] == id_barang:
                return Barang(**barang)
    
    raise HTTPException(status_code=404, detail=f"Barang dengan ID '{id_barang}' tidak ditemukan.")


def tambah_barang(barang_baru: dict) -> Union[dict, Barang]:
    data = read_json(BARANG_PATH)
    kategori = barang_baru["id"][0].upper()
    
    if kategori not in data:
        data[kategori] = []


    for barang in data[kategori]:
        if barang["id"] == barang_baru["id"]:
            return {"error": "Barang dengan ID ini sudah ada"}


    data[kategori].append(barang_baru)
    write_json(BARANG_PATH, data)


    return {"message": "Barang berhasil ditambahkan", "data": barang_baru}


def edit_barang(id_barang: str, data_update: dict) -> dict:
    try:
        data = read_json(BARANG_PATH)


        if not isinstance(data, dict):
            return {"error": "Format data barang tidak valid (bukan dict kategori)"}


        barang_ditemukan = False
        hasil_barang = {}


        for kategori, daftar_barang in data.items():
            for index, barang in enumerate(daftar_barang):
                if barang.get("id") == id_barang:
                    for key, value in data_update.items():
                        if key in barang:
                            data[kategori][index][key] = value
                    barang_ditemukan = True
                    hasil_barang = data[kategori][index]
                    break
            if barang_ditemukan:
                break


        if not barang_ditemukan:
            return {"error": f"Barang dengan ID '{id_barang}' tidak ditemukan."}


        write_json(BARANG_PATH, data)
        return {"message": "Barang berhasil diperbarui", "barang": hasil_barang}
    except Exception as e:
        return {"error": f"Gagal memperbarui barang: {str(e)}"}


def hapus_barang(id_barang: str) -> dict:
    try:
        if not os.path.exists(BARANG_PATH):
            return {"error": "Data file not found."}


        with open(BARANG_PATH, "r") as f:
            data = json.load(f)


        barang_ditemukan = False


        for kategori, daftar_barang in data.items():
            data_baru = []
            for item in daftar_barang:
                if item["id"] == id_barang:
                    barang_ditemukan = True
                    continue
                data_baru.append(item)
            data[kategori] = data_baru


        if not barang_ditemukan:
            return {"error": f"Barang dengan ID '{id_barang}' tidak ditemukan."}


        with open(BARANG_PATH, "w") as f:
            json.dump(data, f, indent=4)


        return {"message": f"Barang dengan ID '{id_barang}' berhasil dihapus."}
    except Exception as e:
        return {"error": str(e)}


def cek_stok_menipis(id_barang: str) -> bool:
    data = read_json(BARANG_PATH)
    for kategori in data.values():
        for barang in kategori:
            if barang["id"] == id_barang:
                return barang["stok"] < 10
    return False
