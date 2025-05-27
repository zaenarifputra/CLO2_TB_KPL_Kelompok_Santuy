import time
import json
from tkinter.font import BOLD
import requests
import subprocess
import sys
from service.stock_service import tambah_barang_ke_file

API_URL = "http://127.0.0.1:8000"

# ANSI color
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BOLD = "\033[1m"
BLUE = "\033[34m"

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
        except Exception:
            time.sleep(1)
    return False

# ================= HEADER =================
def show_header():
    print(f"""{BLUE}
  ╔════════════════════════════════════════════════════╗
  ║                📦 StokLy Inventory CLI             ║
  ║         Sistem Manajemen Inventaris Barang         ║
  ╚════════════════════════════════════════════════════╝{RESET}
    """)

# ============== MENU FUNGSI ==============
def lihat_barang():
    try:
        res = requests.get(f"{API_URL}/stok/stok/stok/")
        res.raise_for_status()
        response = res.json()

        # Pastikan response memiliki data dan berupa list
        if "data" not in response or not isinstance(response["data"], list):
            print("Data yang diterima tidak sesuai format (diharapkan list of barang).")
            return

        # Ubah dari list menjadi dict per kategori (agar tampilan tidak berubah)
        kategori_map = {}
        for barang in response["data"]:
            kategori = barang.get("kategori", "Lainnya").capitalize()
            if kategori not in kategori_map:
                kategori_map[kategori] = []
            kategori_map[kategori].append(barang)

        print(f"\n📋 {YELLOW}DAFTAR BARANG - StokLy Inventory CLI{RESET}")

        for kategori, daftar in kategori_map.items():
            if not isinstance(daftar, list):
                continue

            print(f"\nKategori: {GREEN}{kategori.upper()}{RESET}")
            print("-" * 80)
            print(f"{'ID':<10} {'Nama Barang':<30} {'Berat':<10} {'Harga':<10} {'Stok':<5}")
            print("-" * 80)

            for barang in daftar:
                if not isinstance(barang, dict):
                    continue
                print(f"{barang.get('id', ''):<10} {barang.get('nama', ''):<30} {barang.get('berat', ''):<10} "
                      f"Rp{barang.get('harga', 0):<9} {barang.get('stok', 0):<5}")
            print("-" * 80)

    except Exception as e:
        print(f"{RED}Gagal mengambil data: {e}{RESET}")


def tambah_barang_cli():
    try:
        print(f"{GREEN}➕ Tambah Barang Baru:{RESET}")
        data = {
            "id": input("ID Barang: "),
            "nama": input("Nama Barang: "),
            "harga": int(input("Harga Barang: ")),
            "berat": input("Berat: "),
            "stok": int(input("Stok: ")),
        }
        kategori = input("Kategori Barang (misal: BR): ")
        result = tambah_barang_ke_file(data, kategori)
        print(f"{GREEN}Barang berhasil ditambahkan!{RESET}")
        
        # Menampilkan daftar barang setelah barang baru ditambahkan
        print(f"\n📋 DAFTAR BARANG - StokLy Inventory CLI\n")
        res = requests.get(f"{API_URL}/stok/stok/stok/")
        res.raise_for_status()
        data = res.json()

        for kategori, daftar in data.items():
            if not isinstance(daftar, list):
                continue

            print(f"Kategori: {GREEN}{kategori.upper()}{RESET}")
            print("-" * 80)
            print(f"{'ID':<10} {'Nama Barang':<30} {'Berat':<10} {'Harga':<10} {'Stok':<5}")
            print("-" * 80)

            for barang in daftar:
                if not isinstance(barang, dict):
                    continue
                print(f"{barang.get('id', ''):<10} {barang.get('nama', ''):<30} {barang.get('berat', ''):<10} "
                      f"Rp{barang.get('harga', 0):<9} {barang.get('stok', 0):<5}")
            print("-" * 80)
            
    except ValueError:
        print(f"{RED}Input harga atau stok harus berupa angka.{RESET}")
    except Exception as e:
        print(f"{RED}Gagal menambah barang: {e}{RESET}")

def edit_barang():
    print(f"{YELLOW}✏️ Edit Barang:{RESET}")
    id_barang = input("ID Barang yang ingin diedit: ")
    print("Masukkan data baru (kosongkan jika tidak ingin mengubah):")

    update_data = {"id": id_barang}  # Pastikan ID disertakan dalam body

    nama = input("Nama baru: ")
    harga = input("Harga baru: ")
    berat = input("Berat baru: ")
    stok = input("Stok baru: ")
    kategori = input("Kategori (kosongkan jika tidak ingin mengubah): ")

    if nama: update_data["nama"] = nama
    if harga: 
        try:
            update_data["harga"] = int(harga)
        except ValueError:
            print(f"{RED}❌ Harga harus berupa angka.{RESET}")
            return
    if berat: update_data["berat"] = berat
    if stok: 
        try:
            update_data["stok"] = int(stok)
        except ValueError:
            print(f"{RED}❌ Stok harus berupa angka.{RESET}")
            return
    if kategori: update_data["kategori"] = kategori

    if len(update_data) == 1:  # hanya berisi "id"
        print(f"{YELLOW}⚠️ Tidak ada data yang diubah.{RESET}")
        return

    try:
        print(f"{CYAN}\n🔄 Mengirim data ke API...{RESET}")
        print(update_data)

        res = requests.put(f"{API_URL}/stok/stok/stok/{id_barang}", json=update_data)
        res.raise_for_status()
        updated_barang = res.json()

        print(f"{GREEN}✅ Barang berhasil diperbarui!{RESET}")

        # Menampilkan detail barang terbaru
        print(f"\n📋 DAFTAR BARANG - StokLy Inventory CLI")
        kategori = updated_barang.get("kategori", "Tidak diketahui")
        print(f"\nKategori: {GREEN}{kategori.upper()}{RESET}")
        print("-" * 80)
        print(f"{'ID':<10} {'Nama Barang':<30} {'Berat':<10} {'Harga':<10} {'Stok':<5}")
        print("-" * 80)
        print(f"{updated_barang.get('id', ''):<10} {updated_barang.get('nama', ''):<30} "
              f"{updated_barang.get('berat', ''):<10} Rp{updated_barang.get('harga', 0):<9} "
              f"{updated_barang.get('stok', 0):<5}")
        print("-" * 80)

    except requests.exceptions.RequestException as e:
        print(f"{RED}❌ Gagal mengedit barang: {e}{RESET}")
        if e.response is not None:
            print(f"{YELLOW}Respons API: {e.response.json()}{RESET}")



def hapus_barang():
    print(f"{RED}🗑️ Hapus Barang:{RESET}")
    id_barang = input("ID Barang yang ingin dihapus: ")
    try:
        res = requests.delete(f"{API_URL}/stok/stok/stok{id_barang}")
        res.raise_for_status()
        data = res.json()

        if res.status_code == 200:
            print(f"{GREEN}Barang dengan ID {id_barang} berhasil dihapus!{RESET}")
        else:
            print(f"{YELLOW}Tidak ada barang yang dihapus. Periksa ID yang dimasukkan.{RESET}")

        # Tampilkan ulang daftar barang setelah penghapusan
        lihat_barang()

    except requests.exceptions.HTTPError as http_err:
        print(f"{RED}Gagal menghapus barang: {http_err}{RESET}")
    except Exception as e:
        print(f"{RED}Terjadi kesalahan: {e}{RESET}")


def cari_barang():
    keyword = input("🔍 Masukkan nama barang yang dicari: ").lower()
    try:
        res = requests.get(f"{API_URL}/stok/stok/stok/")
        res.raise_for_status()
        hasil = []

        for kategori, daftar in res.json().items():
            for b in daftar:
                if isinstance(b, dict) and keyword in b.get("nama", "").lower():
                    b["kategori"] = kategori.upper()
                    hasil.append(b)

        if hasil:
            print(f"{GREEN}📋 HASIL PENCARIAN BARANG - StokLy Inventory CLI{RESET}\n")

            for kategori in set([item["kategori"] for item in hasil]):
                print(f"{BOLD}Kategori: {kategori}{RESET}")
                print("-" * 80)
                print(f"{'ID':<10} {'Nama Barang':<30} {'Berat':<10} {'Harga':<12} {'Stok'}")
                print("-" * 80)
                for item in hasil:
                    if item["kategori"] == kategori:
                        print(f"{item['id']:<10} {item['nama']:<30} {item['berat']:<10} Rp{item['harga']:<10,} {item['stok']}")
                print("-" * 80)
        else:
            print(f"{YELLOW}Barang tidak ditemukan.{RESET}")
    except Exception as e:
        print(f"{RED}Gagal mencari barang: {e}{RESET}")

def laporan_inventaris():
    try:
        print(f"{GREEN}📈 LAPORAN BARANG TERLARIS - StokLy Inventory CLI{RESET}\n")
        res = requests.get(f"{API_URL}/analisis")
        res.raise_for_status()
        
        laporan = res.json()

        # Cek status dan pastikan ada data dalam response
        if laporan.get('status') == 'success' and laporan.get('data'):
            laporan_data = laporan['data']

            # Menampilkan hasil laporan jika ada
            print(f"{'ID Barang':<12} {'Jumlah Terjual':<15}")
            print("-" * 40)
            for item in laporan_data:
                print(f"{item['id']:<12} {item['jumlah']:<15}")
            print("-" * 40)
        else:
            print(f"{YELLOW}Tidak ada data laporan tersedia.{RESET}")

    except Exception as e:
        print(f"{RED}Gagal mengambil laporan: {e}{RESET}")

def notif_stok_menipis():
    try:
        print(f"{YELLOW}⚠️ NOTIFIKASI STOK MENIPIS - StokLy Inventory CLI{RESET}")
        res = requests.get(f"{API_URL}/notifikasi/stok/stok/")
        res.raise_for_status()
        data = res.json().get("stok_menipis", [])

        if not isinstance(data, list):
            print(f"{RED}Format data stok_menipis tidak valid: {data}{RESET}")
            return

        if not data:
            print(f"{YELLOW}Tidak ada barang dengan stok menipis.{RESET}")
            return

        print(f"{'ID':<12} {'Nama Barang':<30} {'Stok':<6}")
        print("-" * 60)
        for item in data:
            print(f"{item.get('id', ''):<12} {item.get('nama', ''):<30} {item.get('stok', ''):<6}")
        print("-" * 60)

    except Exception as e:
        print(f"{RED}Gagal mengambil notifikasi: {e}{RESET}")

def lihat_kategori():
    try:
        print(f"{BLUE}🏷️ DAFTAR KATEGORI - StokLy Inventory CLI{RESET}\n")
        res = requests.get(f"{API_URL}/kategori")
        res.raise_for_status()

        response = res.json()

        # Mengakses data kategori dari respons
        kategori_list = response.get('data', [])

        if kategori_list:
            print(f"{'Kode':<10} {'Nama Kategori':<30}")
            print("-" * 45)
            for kat in kategori_list:
                print(f"{kat.get('idKategori', ''):<10} {kat.get('nama', ''):<30}")
            print("-" * 45)
        else:
            print(f"{YELLOW}Tidak ada kategori yang tersedia atau format data tidak sesuai.{RESET}")

    except Exception as e:
        print(f"{RED}Gagal mengambil kategori: {e}{RESET}")



def tambah_transaksi():
    print(f"{GREEN}🧾 TAMBAH TRANSAKSI - StokLy Inventory CLI{RESET}")
    try:
        data = {
            "barang_id": input("ID Barang: "),
            "tipe": input("Tipe (masuk/keluar): "),
            "jumlah": int(input("Jumlah: ")),
            "tanggal": input("Tanggal (YYYY-MM-DD): ")
        }

        res = requests.post(f"{API_URL}/transaksi", json=data)
        res.raise_for_status()
        transaksi = res.json()

        print(f"\n{GREEN}✅ Transaksi berhasil ditambahkan!{RESET}")
        print("-" * 80)
        print(f"{'ID Barang':<15} {'Tipe':<10} {'Jumlah':<10} {'Tanggal':<15}")
        print("-" * 80)
        print(f"{transaksi.get('barang_id', ''):<15} "
              f"{transaksi.get('tipe', ''):<10} "
              f"{transaksi.get('jumlah', ''):<10} "
              f"{transaksi.get('tanggal', ''):<15}")
        print("-" * 80)

    except Exception as e:
        print(f"{RED}Gagal menambah transaksi: {e}{RESET}")


def lihat_transaksi():
    try:
        print(f"{YELLOW}📚 DAFTAR TRANSAKSI - StokLy Inventory CLI{RESET}")
        res = requests.get(f"{API_URL}/transaksi")
        res.raise_for_status()  # Memastikan tidak ada error dalam respons

        # Mengambil JSON dari respons
        response = res.json()

        # Mengecek apakah 'data' ada dalam respons
        data = response.get('data', [])

        if not data:
            print(f"{YELLOW}Tidak ada data transaksi.{RESET}")
            return

        print("-" * 100)
        print(f"{'ID Transaksi':<15} {'ID Barang':<15} {'Tipe':<12} {'Jumlah':<10} {'Tanggal':<20}")
        print("-" * 100)
        
        # Menampilkan data transaksi
        for tr in data:
            print(f"{tr.get('id', ''):<15} "
                  f"{tr.get('barang_id', ''):<15} "
                  f"{tr.get('tipe', ''):<12} "
                  f"{tr.get('jumlah', ''):<10} "
                  f"{tr.get('tanggal', ''):<20}")
        print("-" * 100)
    
    except Exception as e:
        print(f"{RED}Gagal mengambil transaksi: {e}{RESET}")


# ============== MAIN MENU ==============
def main_menu():
    while True:
        show_header()
        print("1️⃣  Lihat daftar barang")
        print("2️⃣  Tambah barang")
        print("3️⃣  Edit barang")
        print("4️⃣  Hapus barang")
        print("5️⃣  Cari barang")
        print("6️⃣  Laporan barang terlaris")
        print("7️⃣  Notifikasi stok menipis")
        print("8️⃣  Lihat kategori")
        print("9️⃣  Tambah transaksi")
        print("🔟 Lihat semua transaksi")
        print("0️⃣  Keluar")
        print()

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
            "0": exit
        }

        if choice in menu_map:
            if choice == "0":
                print(f"{GREEN}Terima kasih telah menggunakan StokLy! Sampai jumpa!{RESET}")
                break
            print()
            menu_map[choice]()
            print("\n" + "-"*60 + "\n")
        else:
            print(f"{RED}❌ Pilihan tidak valid. Coba lagi.{RESET}")

# ============= MAIN RUN ==============
if __name__ == "__main__":
    print(f"{YELLOW}🚀 Menjalankan server API...{RESET}")
    start_api_server()
    print(f"{YELLOW}🔄 Mengecek koneksi ke API...{RESET}")
    if wait_for_api():
        print(f"{GREEN}✅ API siap digunakan.{RESET}")
        main_menu()
    else:
        print(f"{RED}❌ Tidak dapat menghubungi API. Periksa koneksi atau port.{RESET}")