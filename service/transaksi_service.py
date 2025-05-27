from schemas.transaksi_schema import Transaksi
from utils.file_manager import read_json, write_json

def catat_transaksi(data: Transaksi) -> Transaksi:
    transaksi_baru = data.dict()
    transaksi_baru["tanggal"] = str(transaksi_baru["tanggal"])

    all_transaksi = read_json("data/transaksi.json")

    transaksi_baru["idTransaksi"] = len(all_transaksi) + 1
    all_transaksi.append(transaksi_baru)

    write_json("data/transaksi.json", all_transaksi)

    return Transaksi(**transaksi_baru)
