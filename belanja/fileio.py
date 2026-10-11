from belanja.model import Barang


def inisialisasi_file(nama_file):
    """
    Mode 'x': Digunakan untuk membuat file baru.
    Jika file sudah ada, FileExistsError muncul tanpa menimpa data yang ada.
    """
    try:
        with open(nama_file, "x", encoding="utf-8") as f:
            pass
        return True
    except FileExistsError:
        return False
    except Exception as e:
        print(f"[Peringatan] Gagal inisialisasi file: {e}")
        return False


def baca_data(nama_file):
    """
    Mode 'r': Digunakan untuk membaca data dari file teks.
    Muncul FileNotFoundError jika file belum dibuat.
    """
    daftar_barang = []
    try:
        with open(nama_file, "r", encoding="utf-8") as f:
            for nomor_baris, baris in enumerate(f, start=1):
                teks = baris.strip()
                if not teks:
                    continue
                bagian = teks.split("|")
                # Format yang diharapkan: id|nama|jumlah|satuan|status|catatan (catatan opsional)
                if len(bagian) >= 5:
                    try:
                        id_barang = int(bagian[0])
                        nama = bagian[1]
                        jumlah = int(bagian[2])
                        satuan = bagian[3]
                        status = bagian[4]
                        catatan = bagian[5] if len(bagian) > 5 else ""

                        barang = Barang(
                            id_barang=id_barang,
                            nama=nama,
                            jumlah=jumlah,
                            satuan=satuan,
                            status=status,
                            catatan=catatan
                        )
                        daftar_barang.append(barang)
                    except (ValueError, IndexError):
                        # Abaikan baris rusak agar program tetap berjalan
                        print(f"[Peringatan] Baris {nomor_baris} di {nama_file} memiliki format tidak valid, dilewati.")
    except FileNotFoundError:
        # Jika file belum ada, otomatis inisialisasi file kosong
        inisialisasi_file(nama_file)
        return []

    return daftar_barang


def tambah_ke_file(nama_file, barang):
    """
    Mode 'a': Digunakan untuk menambahkan baris barang baru di akhir file
    tanpa menimpa atau membaca ulang smua data lama.
    """
    with open(nama_file, "a", encoding="utf-8") as f:
        f.write(barang.to_line())


def simpan_semua(nama_file, daftar_barang):
    """
    Mode 'w': Digunakan untuk menulis ulang seluruh data ke dalam file.
    Cocok digunakan saat ada pembaruan status atau penghapusan barang.
    """
    with open(nama_file, "w", encoding="utf-8") as f:
        for barang in daftar_barang:
            f.write(barang.to_line())


def tulis_laporan(nama_file, isi_laporan):
    """
    Mode 'w': Digunakan untuk menulis laporan ringkasan belanja ke file teks.
    """
    with open(nama_file, "w", encoding="utf-8") as f:
        f.write(isi_laporan)

