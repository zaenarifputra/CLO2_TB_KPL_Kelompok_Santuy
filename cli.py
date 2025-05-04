import subprocess
import time
import json
import requests

from service.stock_service import tambah_barang_ke_file

API_URL = "http://127.0.0.1:8000"

# Tunggu API siap
def wait_for_api(url=API_URL):
    for _ in range(10):
        try:
            requests.get(f"{url}/docs")
            return True
        except Exception as e:
            print(f"Menunggu API... ({e})")
            time.sleep(1)
    return False

# === MENU FUNGSI ===
def lihat_barang():
    try:
        res = requests.get(f"{API_URL}/stok/stok")
        res.raise_for_status()
        data = res.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Gagal mengambil data: {e}")

def tambah_barang_cli():
    id = input("ID Barang: ")
    nama = input("Nama Barang: ")
    harga = input("Harga Barang: ")
    berat = input("Berat: ")
    stok = input("Stok: ")
    kategori = input("Kategori Barang (misal: BR): ")

    try:
        data = {
            "id": id,
            "nama": nama,
            "harga": int(harga),
            "berat": berat,
            "stok": int(stok),
        }

        result_lokal = tambah_barang_ke_file(data, kategori)
        print(json.dumps(result_lokal, indent=2, ensure_ascii=False))

    except ValueError as e:
        print(f"Input tidak valid: {e}")
    except Exception as e:
        print(f"Gagal menambah barang: {e}")



def edit_barang():
    id_barang = input("ID Barang yang ingin diedit: ")
    print("Masukkan data baru (kosongkan jika tidak ingin mengubah):")
    nama = input("Nama baru: ")
    harga = input("Harga baru: ")
    berat = input("Berat baru: ")
    stok = input("Stok baru: ")

    update_data = {"id": id_barang}
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
        data = res.json()
        hasil = []

        for kategori, daftar in data.items():
            for b in daftar:
                if isinstance(b, dict):
                    nama_barang = str(b.get("nama", "")).lower()
                    if keyword in nama_barang:
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
    barang_id = input("ID Barang: ")
    tipe = input("Tipe (masuk/keluar): ")
    jumlah = int(input("Jumlah: "))
    tanggal = input("Tanggal (YYYY-MM-DD): ")
    data = {
        "barang_id": barang_id,
        "tipe": tipe,
        "jumlah": jumlah,
        "tanggal": tanggal
    }
    try:
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

# === MENU UTAMA ===
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
        
        choice = input("Pilih menu: ")
        if choice == "1":
            lihat_barang()
        elif choice == "2":
            tambah_barang_cli()
        elif choice == "3":
            edit_barang()
        elif choice == "4":
            hapus_barang()
        elif choice == "5":
            cari_barang()
        elif choice == "6":
            laporan_inventaris()
        elif choice == "7":
            notif_stok_menipis()
        elif choice == "8":
            lihat_kategori()
        elif choice == "9":
            tambah_transaksi()
        elif choice == "10":
            lihat_transaksi()
        elif choice == "11":
            print("Terima kasih telah menggunakan aplikasi.")
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

# === MAIN PROGRAM ===
if __name__ == "__main__":
    print("Mengecek koneksi ke API...")
    if wait_for_api():
        print("API siap digunakan.")
        main_menu()
    else:
        print("Tidak dapat menghubungi API. Pastikan server berjalan.")
