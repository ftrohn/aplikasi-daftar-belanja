import unittest

from belanja.model import Barang
from belanja.validasi import validasi_nama, validasi_jumlah, validasi_satuan, validasi_id_ada
from belanja.processing import (
    tambah_barang,
    cari_barang,
    urutkan_barang,
    ubah_status_barang,
    hapus_barang,
    hitung_ringkasan,
)
from belanja.fileio import (
    inisialisasi_file,
    baca_data,
    tambah_ke_file,
    simpan_semua,
)


class TestAplikasiBelanja(unittest.TestCase):
    def setUp(self):
        # Data uji dummy terpisah dalam memori
        self.barang1 = Barang(id_barang=1, nama="Beras Ramos", jumlah=5, satuan="kg", status="Sudah Dibeli", catatan="Pulen")
        self.barang2 = Barang(id_barang=2, nama="Minyak Goreng", jumlah=2, satuan="liter", status="Belum Dibeli")
        self.barang3 = Barang(id_barang=3, nama="Gula Pasir", jumlah=1, satuan="kg", status="Belum Dibeli")
        self.daftar_uji = [self.barang1, self.barang2, self.barang3]

        # File uji terpisah untuk menguji file I/O
        self.file_uji = "test_data_temp.txt"
        with open(self.file_uji, "w", encoding="utf-8") as f:
            pass

    def tearDown(self):
        # Mengosongkan file uji setelah pengujian selesai
        try:
            with open(self.file_uji, "w", encoding="utf-8") as f:
                pass
        except Exception:
            pass

    # 1. Uji pembuatan objek barang
    def test_pembuatan_objek_barang(self):
        b = Barang(id_barang=10, nama="Kopi Bubuk", jumlah=2, satuan="bungkus", status="Belum Dibeli", catatan="Robusta")
        self.assertEqual(b.id_barang, 10)
        self.assertEqual(b.nama, "Kopi Bubuk")
        self.assertEqual(b.jumlah, 2)
        self.assertEqual(b.satuan, "bungkus")
        self.assertEqual(b.status, "Belum Dibeli")
        self.assertEqual(b.catatan, "Robusta")

    # 2. Uji validasi barang
    def test_validasi_barang(self):
        # Nama valid dan tidak valid
        self.assertEqual(validasi_nama("  Susu UHT  "), "Susu UHT")
        with self.assertRaises(ValueError):
            validasi_nama("")
        with self.assertRaises(ValueError):
            validasi_nama("   ")

        # Jumlah valid dan tidak valid
        self.assertEqual(validasi_jumlah(5), 5)
        self.assertEqual(validasi_jumlah("10"), 10)
        with self.assertRaises(ValueError):
            validasi_jumlah(0)
        with self.assertRaises(ValueError):
            validasi_jumlah(-3)
        with self.assertRaises(ValueError):
            validasi_jumlah("bukan_angka")

        # Satuan valid dan tidak valid
        self.assertEqual(validasi_satuan("botol"), "botol")
        with self.assertRaises(ValueError):
            validasi_satuan("  ")

        # ID ditemukan dan tidak ditemukan
        ditemukan = validasi_id_ada(1, self.daftar_uji)
        self.assertEqual(ditemukan.nama, "Beras Ramos")
        with self.assertRaises(ValueError):
            validasi_id_ada(99, self.daftar_uji)

    # 3. Uji pencarian barang
    def test_pencarian_barang(self):
        # Pencarian case-insensitive dan sebagian kata
        hasil_minyak = cari_barang(self.daftar_uji, "minyak")
        self.assertEqual(len(hasil_minyak), 1)
        self.assertEqual(hasil_minyak[0].id_barang, 2)

        hasil_beras = cari_barang(self.daftar_uji, "RAMOS")
        self.assertEqual(len(hasil_beras), 1)
        self.assertEqual(hasil_beras[0].nama, "Beras Ramos")

        # Pencarian tidak ditemukan
        hasil_kosong = cari_barang(self.daftar_uji, "sabun")
        self.assertEqual(len(hasil_kosong), 0)

    # 4. Uji pengurutan barang
    def test_pengurutan_barang(self):
        # Urut A-Z berdasarkan nama: Beras Ramos, Gula Pasir, Minyak Goreng
        hasil_urut = urutkan_barang(self.daftar_uji)
        nama_urut = [b.nama for b in hasil_urut]
        self.assertEqual(nama_urut, ["Beras Ramos", "Gula Pasir", "Minyak Goreng"])

    # 5. Uji perhitungan ringkasan
    def test_perhitungan_ringkasan(self):
        ringkasan = hitung_ringkasan(self.daftar_uji)
        self.assertEqual(ringkasan["total"], 3)
        self.assertEqual(ringkasan["sudah"], 1)
        self.assertEqual(ringkasan["belum"], 2)
        self.assertAlmostEqual(ringkasan["persentase"], 33.33, places=2)

        # Uji daftar kosong
        ringkasan_kosong = hitung_ringkasan([])
        self.assertEqual(ringkasan_kosong["total"], 0)
        self.assertEqual(ringkasan_kosong["sudah"], 0)
        self.assertEqual(ringkasan_kosong["belum"], 0)
        self.assertEqual(ringkasan_kosong["persentase"], 0.0)

    # 6. Uji perubahan status dan penghapusan barang
    def test_ubah_dan_hapus_barang(self):
        # Toggle status dari Belum Dibeli menjadi Sudah Dibeli
        ubah_status_barang(self.daftar_uji, id_barang=2)
        self.assertEqual(self.barang2.status, "Sudah Dibeli")

        # Toggle kembali ke Belum Dibeli
        ubah_status_barang(self.daftar_uji, id_barang=2)
        self.assertEqual(self.barang2.status, "Belum Dibeli")

        # Hapus barang
        dihapus = hapus_barang(self.daftar_uji, id_barang=3)
        self.assertEqual(dihapus.id_barang, 3)
        self.assertEqual(len(self.daftar_uji), 2)

    # 7. Uji operasi file (mode x, a, r, w)
    def test_fileio_dan_mode(self):
        # Uji inisialisasi file (mode x menangkap file yang sudah ada agar tidak tertimpa)
        self.assertFalse(inisialisasi_file(self.file_uji))

        # Uji tambah ke file (mode a)
        tambah_ke_file(self.file_uji, self.barang1)
        tambah_ke_file(self.file_uji, self.barang2)

        # Uji baca dari file (mode r)
        dibaca = baca_data(self.file_uji)
        self.assertEqual(len(dibaca), 2)
        self.assertEqual(dibaca[0].nama, "Beras Ramos")

        # Uji simpan semua / overwrite (mode w)
        simpan_semua(self.file_uji, [self.barang3])
        dibaca_baru = baca_data(self.file_uji)
        self.assertEqual(len(dibaca_baru), 1)
        self.assertEqual(dibaca_baru[0].nama, "Gula Pasir")


if __name__ == "__main__":
    unittest.main()

