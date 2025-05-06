import unittest
from fastapi.testclient import TestClient
from app import app  # pastikan app sudah terimport dengan benar


class TestAppIntegration(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    # Unit Test Stok
    # 1
    # Test untuk mendapatkan semua produk
    def test_get_stok(self):
        response = self.client.get("/stok/barang/BR01")
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())
        self.assertEqual(response.json()["data"]["id"], "BR01")

# 2
    # Test untuk menambahkan produk
    def test_add_stok(self):
        product = {
            "id": "BR06",
            "nama": "Beras Premium",
            "harga": 100000,
            "berat": "5 Kg",
            "stok": 30
        }
        response = self.client.post("/stok/", json=product)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["id"], "BR06")

# 3
    # Test untuk memperbarui produk
    def test_update_stok(self):
        updated_product = {
            "id": "BR06",
            "nama": "Beras Premium Purwokerto",
            "harga": 110000,
            "berat": "5 Kg",
            "stok": 25
        }
        response = self.client.put("/stok/BR06", json=updated_product)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")  # Pastikan status ada di response
        self.assertEqual(response.json()["data"]["id"], "BR06")
        self.assertEqual(response.json()["data"]["nama"], "Beras Premium Purwokerto")
        self.assertEqual(response.json()["data"]["stok"], 25)

# 4 
    # Test untuk menghapus produk
    def test_delete_stok(self):
        response = self.client.delete("/stok/BR06")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(response.json()["message"], "Product BR06 deleted")

    # Unit Test Notifikasi
    # 5 Test untuk mendapatkan semua notifikasi

    def test_get_notifikasi(self):
        response = self.client.get("/notifikasi/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())  

        self.assertIsInstance(response.json()["data"], list)  # Pastikan data adalah list
        self.assertGreater(len(response.json()["data"]), 0)  # Pastikan ada notifikasi

# Unit test untuk kategori
class TestKategoriController(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

# 6
    # Test untuk mendapatkan semua kategori
    def test_get_all_kategori(self):
        # Mengirimkan permintaan GET ke endpoint /kategori/
        response = self.client.get("/kategori/")
        
        # Pastikan status code yang dikembalikan adalah 200
        self.assertEqual(response.status_code, 200)

        # Pastikan format response adalah JSON dan ada field 'data'
        response_data = response.json()
        self.assertIn("data", response_data)

        # Pastikan 'data' adalah list
        self.assertIsInstance(response_data["data"], list)

        # Pastikan ada kategori dengan nama "Beras" dan idKategori "BR"
        kategori_beras = next((k for k in response_data["data"] if k["idKategori"] == "BR"), None)
        self.assertIsNotNone(kategori_beras)
        self.assertEqual(kategori_beras["nama"], "Beras")
        
        # Pastikan ada beberapa kategori
        self.assertGreater(len(response_data["data"]), 0)

# Unit test untuk analisis
class TestAnalisisController(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

# 7
    # Test untuk mendapatkan barang terlaris
    def test_get_barang_terlaris(self):
        response = self.client.get("/analisis/")
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data["status"], "success")
        self.assertEqual(response_data["message"], "Barang terlaris berhasil ditampilkan")
        self.assertIn("data", response_data)

        # Pastikan data berupa list dan isinya maksimal 3 item
        self.assertIsInstance(response_data["data"], list)
        self.assertLessEqual(len(response_data["data"]), 3)

        # Pastikan setiap item dalam data memiliki 'id_barang' dan 'total_terjual'
        for item in response_data["data"]:
            self.assertIn("id", item)
            self.assertIn("jumlah", item)
    

    # Unit test untuk transaksi
class TestTransaksiController(unittest.TestCase): 

    def setUp(self):
        self.client = TestClient(app)

# 8
    # Test untuk mendapatkan semua transaksi

    def test_get_transaksi(self):
        response = self.client.get("/transaksi/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())  

    

            

if __name__ == "__main__":
    unittest.main()






