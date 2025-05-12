from ctypes.wintypes import MAX_PATH
from fastapi import HTTPException
from schemas.barang_schema import Barang
from utils.file_manager import read_json, write_json
from utils.validator import valid_id_barang
from typing import Union
from schemas.barang_schema import Barang 
from utils.file_manager import read_json, write_json 
import importlib
import json
import os


BARANG_PATH = "data/barang.json"


def get_all_barang() -> list:
    return read_json(BARANG_PATH)


def get_barang_by_id(id: str) -> Barang:
    try:
        semua_barang = read_json("data/barang.json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal membaca file JSON: {str(e)}")

    for kategori in semua_barang.values():
        for barang_dict in kategori:
            if barang_dict.get("id") == id:
                try:
                    return Barang(**barang_dict)
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Data tidak valid: {str(e)}")

    raise HTTPException(status_code=404, detail=f"Barang dengan ID '{id}' tidak ditemukan.")


def tambah_barang(barang: dict, kategori: str):
    data_barang = read_json("data/barang.json")
    
    if kategori not in data_barang:
        data_barang[kategori] = []
    
    for existing_barang in data_barang[kategori]:
        if existing_barang["id"] == barang["id"]:
            return {"error": f"Barang dengan ID '{barang['id']}' sudah ada dalam kategori '{kategori}'."}
    
    data_barang[kategori].append(barang)
    data_barang[kategori].sort(key=lambda x: x["id"])
    
    write_json("data/barang.json", data_barang)
    
    return {
        "message": f"Barang dengan ID '{barang['id']}' berhasil ditambahkan ke kategori '{kategori}'.",
        "data": barang
    }

def tambah_barang_ke_file(barang: dict, kategori: str):
    from utils.file_manager import read_json, write_json

    data_barang = read_json("data/barang.json")

    if kategori not in data_barang:
        data_barang[kategori] = []

    for existing_barang in data_barang[kategori]:
        if existing_barang["id"] == barang["id"]:
            return {"error": f"Barang dengan ID '{barang['id']}' sudah ada dalam kategori '{kategori}'."}

    data_barang[kategori].append(barang)
    data_barang[kategori].sort(key=lambda x: x["id"])

    write_json("data/barang.json", data_barang)

    return {
        "message": f"Barang dengan ID '{barang['id']}' berhasil ditambahkan ke kategori '{kategori}'.",
        "data": barang
    }


def edit_barang(id_barang: str, data_update: dict):
    data_barang = read_json("data/barang.json")
    barang_ditemukan = None
    for kategori, daftar_barang in data_barang.items():
        for i, barang in enumerate(daftar_barang):
            if barang["id"] == id_barang:
                data_barang[kategori][i].update(data_update)
                barang_ditemukan = data_barang[kategori][i]
                break
        if barang_ditemukan:
            break
    if not barang_ditemukan:
        return {"error": f"Barang dengan ID '{id_barang}' tidak ditemukan."}
    write_json("data/barang.json", data_barang)
    return {
        "message": f"Barang dengan ID '{id_barang}' berhasil diperbarui.",
        "barang": barang_ditemukan
    }

def hapus_barang(id_barang: str):
    data_barang = read_json("data/barang.json")
    barang_dihapus = None

    for kategori, daftar_barang in data_barang.items():
        for i, barang in enumerate(daftar_barang):
            if barang["id"] == id_barang:
                barang_dihapus = data_barang[kategori].pop(i)
                break
        if barang_dihapus:
            break

    if not barang_dihapus:
        return {"error": f"Barang dengan ID '{id_barang}' tidak ditemukan."}

    write_json("data/barang.json", data_barang)
    return {
        "message": f"Barang dengan ID '{id_barang}' berhasil dihapus.",
        "data": barang_dihapus
    }


def cek_stok_menipis(id_barang: str) -> bool:
    data = read_json(BARANG_PATH)
    for barang in data:
        if barang["id"] == id_barang:
            return barang["stok"] < 10
    return False