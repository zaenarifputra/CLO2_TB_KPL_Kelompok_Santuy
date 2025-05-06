import time
import json
import requests
import subprocess
import sys
from service.stock_service import tambah_barang_ke_file

API_URL = "http://127.0.0.1:8000"

def start_api_server():
    """Menjalankan server FastAPI secara otomatis di background."""
    subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app:app", "--reload"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def wait_for_api(url=API_URL):
    """Menunggu API FastAPI hingga siap."""
    for _ in range(15):
        try:
            res = requests.get(f"{url}/docs")
            if res.status_code == 200:
                return True
        except Exception as e:
            print(f"Menunggu API... ({e})")
            time.sleep(1)
    return False

# ======== FUNGSI MENU ========
def lihat_barang():
    try:
        res = requests.get(f"{API_URL}/stok/stok")
        res.raise_for_status()
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Gagal mengambil data: {e}")

def tambah_barang_cli():
    try:
        data = {
            "id": input("ID Barang: "),
            "nama": input("Nama Barang: "),
            "harga": int(input("Harga Barang: ")),
            "berat": input("Berat: "),
            "stok": int(input("Stok: ")),
        }
        kategori = input("Kategori Barang (misal: BR): ")
        result = tambah_barang_ke_file(data, kategori)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except ValueError:
        print("Input harga atau stok harus berupa angka.")
    except Exception as e:
        print(f"Gagal menambah barang: {e}")

def edit_barang():
    id_barang = input("ID Barang yang ingin diedit: ")
    print("Masukkan data baru (kosongkan jika tidak ingin mengubah):")
    update_data = {"id": id_barang}

    nama = input("Nama baru: ")
    harga = input("Harga baru: ")
    berat = input("Berat baru: ")
    stok = input("Stok baru: ")

    if nama: update_data["nama"] = nama
    if harga: update_data["harga"] = int(harga)
    if berat: update_data["berat"] = berat
    if stok: update_data["stok"] = int(stok)

    try:
        res = requests.put(f"{API_URL}/stok/stok/{id_barang}", json=update_data)
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Gagal mengedit barang: {e}")

def hapus_barang():
    id_barang = input("ID Barang yang ingin dihapus: ")
    try:
        res = requests.delete(f"{API_URL}/stok/stok/{id_barang}")
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Gagal menghapus barang: {e}")

def cari_barang():
    keyword = input("Masukkan nama barang yang dicari: ").lower()
    try:
        res = requests.get(f"{API_URL}/stok/stok")
        res.raise_for_status()
        hasil = []

        for kategori, daftar in res.json().items():
            for b in daftar:
                if isinstance(b, dict) and keyword in b.get("nama", "").lower():
                    hasil.append(b)

        if hasil:
            print(json.dumps(hasil, indent=2, ensure_ascii=False))
        else:
            print("Barang tidak ditemukan.")
    except Exception as e:
        print(f"Gagal mencari barang: {e}")

def laporan_inventaris():
    try:
        res = requests.get(f"{API_URL}/analisis")
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Gagal mengambil laporan: {e}")

def notif_stok_menipis():
    try:
        res = requests.get(f"{API_URL}/notifikasi/stok")
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Gagal mengambil notifikasi: {e}")

def lihat_kategori():
    try:
        res = requests.get(f"{API_URL}/kategori")
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Gagal mengambil kategori: {e}")

def tambah_transaksi():
    try:
        data = {
            "barang_id": input("ID Barang: "),
            "tipe": input("Tipe (masuk/keluar): "),
            "jumlah": int(input("Jumlah: ")),
            "tanggal": input("Tanggal (YYYY-MM-DD): ")
        }
        res = requests.post(f"{API_URL}/transaksi", json=data)
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Gagal menambah transaksi: {e}")

def lihat_transaksi():
    try:
        res = requests.get(f"{API_URL}/transaksi")
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Gagal mengambil transaksi: {e}")

# ========= MAIN MENU =========
def main_menu():
    while True:
        print("\n=== MENU UTAMA INVENTARIS BARANG ===")
        print("1. Lihat daftar barang")
        print("2. Tambah barang")
        print("3. Edit barang")
        print("4. Hapus barang")
        print("5. Cari barang")
        print("6. Laporan barang terlaris")
        print("7. Notifikasi stok menipis")
        print("8. Lihat kategori")
        print("9. Tambah transaksi")
        print("10. Lihat semua transaksi")
        print("11. Keluar")

        choice = input("Pilih menu: ").strip()
        menu_map = {
            "1": lihat_barang,
            "2": tambah_barang_cli,
            "3": edit_barang,
            "4": hapus_barang,
            "5": cari_barang,
            "6": laporan_inventaris,
            "7": notif_stok_menipis,
            "8": lihat_kategori,
            "9": tambah_transaksi,
            "10": lihat_transaksi,
            "11": exit
        }

        if choice in menu_map:
            if choice == "11":
                print("Terima kasih telah menggunakan aplikasi StokLy - Sistem Manajemen Inventaris.")
                break
            menu_map[choice]()
        else:
            print("Pilihan tidak valid. Coba lagi.")

# ========== MAIN =============
if __name__ == "__main__":
    print("Menjalankan server API secara otomatis...")
    start_api_server()
    print("Mengecek koneksi ke API...")
    if wait_for_api():
        print("API siap digunakan.")
        main_menu()
    else:
        print("Tidak dapat menghubungi API. Pastikan tidak ada masalah port atau script.")
