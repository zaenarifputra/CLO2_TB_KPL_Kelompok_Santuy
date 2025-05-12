import unittest
from fastapi.testclient import TestClient
from app import app

class TestAppIntegration(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    # ----------------- Stok -----------------

    def test_get_stok_success(self):
        response = self.client.get("/stok/barang/BR01")
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())
        self.assertEqual(response.json()["data"]["id"], "BR01")

    def test_get_stok_not_found(self):
        response = self.client.get("/stok/barang/BR99")
        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"], "Product not found")

    def test_add_stok_success(self):
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

    def test_add_stok_invalid(self):
        product = {
            "id": "BR06",
            "nama": "Beras Premium",
            "harga": 100000,
            "berat": "5 Kg",
            "stok": -10
        }
        response = self.client.post("/stok/", json=product)
        self.assertEqual(response.status_code, 422)

    def test_update_stok_success(self):
        updated_product = {
            "id": "BR06",
            "nama": "Beras Premium Purwokerto",
            "harga": 110000,
            "berat": "5 Kg",
            "stok": 25
        }
        response = self.client.put("/stok/BR06", json=updated_product)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(response.json()["data"]["id"], "BR06")
        self.assertEqual(response.json()["data"]["stok"], 25)

    def test_update_stok_not_found(self):
        updated_product = {
            "id": "BR99",
            "nama": "Beras Premium Purwokerto",
            "harga": 110000,
            "berat": "5 Kg",
            "stok": 25
        }
        response = self.client.put("/stok/BR99", json=updated_product)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Product not found")

    def test_delete_stok_success(self):
        response = self.client.delete("/stok/BR06")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(response.json()["message"], "Product BR06 deleted")

    def test_delete_stok_not_found(self):
        response = self.client.delete("/stok/BR99")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Product not found")

    # ----------------- Notifikasi -----------------

    def test_get_notifikasi(self):
        response = self.client.get("/notifikasi/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())
        self.assertIsInstance(response.json()["data"], list)

    def test_get_notifikasi_empty(self):
        response = self.client.get("/notifikasi/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())
        self.assertEqual(len(response.json()["data"]), 0)

    # ----------------- Kategori -----------------

class TestKategoriController(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_all_kategori(self):
        response = self.client.get("/kategori/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())
        self.assertIsInstance(response.json()["data"], list)
        self.assertGreaterEqual(len(response.json()["data"]), 0)

    

    # ----------------- Analisis -----------------

class TestAnalisisController(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_barang_terlaris(self):
        response = self.client.get("/analisis/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("data", data)
        self.assertIsInstance(data["data"], list)
        if len(data["data"]) > 0:
            self.assertIn("id", data["data"][0])
            self.assertIn("jumlah", data["data"][0])

    
    def test_get_barang_terlaris_empty(self):
        response = self.client.get("/analisis/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())

    # ----------------- Transaksi -----------------

class TestTransaksiController(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_transaksi(self):
        response = self.client.get("/transaksi/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())


    


if __name__ == "__main__":
    unittest.main()
