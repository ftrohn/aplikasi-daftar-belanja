from datetime import datetime
from belanja.model import Barang
from belanja.validasi import validasi_nama, validasi_jumlah, validasi_satuan, validasi_id_ada


def format_baris_tabel(*args):
    """
    *args untuk menerima jumlah kolom fleksibel dan
    menggabungkannya menjadi satu baris tampilan rapi.
    """
    lebar_kolom = [4, 25, 8, 10, 15, 20]
    bagian = []
    for indeks, teks in enumerate(args):
        lebar = lebar_kolom[indeks] if indeks < len(lebar_kolom) else 15
        bagian.append(f"{str(teks):<{lebar}}")
    return " | ".join(bagian)


def tambah_barang(daftar_barang, nama, jumlah, satuan, **kwargs):
    """
    Menambahkan barang baru dengan validasi dan kwargs untuk opsi tambahan (misal catatan).
    """
    assert isinstance(daftar_barang, list), "daftar_barang harus berupa list"

    nama_valid = validasi_nama(nama)
    jumlah_valid = validasi_jumlah(jumlah)
    satuan_valid = validasi_satuan(satuan)

    # Menentukan ID baru secara otomatis agar selalu unik
    id_baru = max([b.id_barang for b in daftar_barang], default=0) + 1

    # Menggunakan keyword arguments saat memanggil constructor Barang
    barang_baru = Barang(
        id_barang=id_baru,
        nama=nama_valid,
        jumlah=jumlah_valid,
        satuan=satuan_valid,
        status="Belum Dibeli",
        **kwargs
    )
    daftar_barang.append(barang_baru)
    return barang_baru


def cari_barang(daftar_barang, kata_kunci):
    assert isinstance(daftar_barang, list), "daftar_barang harus berupa list"
    kunci = str(kata_kunci).strip().lower()
    hasil = [b for b in daftar_barang if kunci in b.nama.lower()]
    return hasil


def urutkan_barang(daftar_barang, **kwargs):
    """
    Menggunakan lambda untuk mengurutkan daftar barang berdasarkan nama barang (case-insensitive).
    Mendukung opsi reverse melalui kwargs.
    """
    assert isinstance(daftar_barang, list), "daftar_barang harus berupa list"
    mundur = kwargs.get("reverse", False)
    return sorted(daftar_barang, key=lambda b: b.nama.lower(), reverse=mundur)


def ubah_status_barang(daftar_barang, id_barang, status_baru=None):
    barang = validasi_id_ada(id_barang, daftar_barang)
    if status_baru is None:
        # Toggle otomatis jika status_baru tidak ditentukan
        if barang.status == "Sudah Dibeli":
            barang.tandai_belum_dibeli()
        else:
            barang.tandai_sudah_dibeli()
    else:
        barang.ubah_status(status_baru)
    return barang


def hapus_barang(daftar_barang, id_barang):
    barang = validasi_id_ada(id_barang, daftar_barang)
    daftar_barang.remove(barang)
    return barang


def hitung_ringkasan(daftar_barang):
    assert isinstance(daftar_barang, list), "daftar_barang harus berupa list"

    total = len(daftar_barang)
    sudah = sum(1 for b in daftar_barang if b.status == "Sudah Dibeli")
    belum = total - sudah
    persentase = (sudah / total * 100) if total > 0 else 0.0

    # Pemeriksaan konsistensi internal dengan assert
    assert sudah <= total, "Jumlah barang yang sudah dibeli tidak boleh melebihi total barang"

    return {
        "total": total,
        "sudah": sudah,
        "belum": belum,
        "persentase": round(persentase, 2)
    }


def buat_teks_laporan(daftar_barang, ringkasan):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    garis = "=" * 75

    baris_laporan = [
        garis,
        "                     LAPORAN DAFTAR BELANJA",
        garis,
        f"Waktu Dibuat : {waktu}",
        f"Total Barang : {ringkasan['total']}",
        f"Sudah Dibeli : {ringkasan['sudah']}",
        f"Belum Dibeli : {ringkasan['belum']}",
        f"Penyelesaian : {ringkasan['persentase']}%",
        garis,
        format_baris_tabel("ID", "Nama Barang", "Jumlah", "Satuan", "Status", "Catatan"),
        "-" * 75
    ]

    for b in daftar_barang:
        baris_laporan.append(format_baris_tabel(b.id_barang, b.nama, b.jumlah, b.satuan, b.status, b.catatan))

    baris_laporan.append(garis)
    return "\n".join(baris_laporan) + "\n"


if __name__ == "__main__":
    # Pengujian mandiri modul processing
    print("Menjalankan uji mandiri modul processing...")
    sampel = []
    item = tambah_barang(sampel, "Apel Manis", 5, "buah", catatan="Segar")
    print("Barang dibuat:", item)
    ringkasan = hitung_ringkasan(sampel)
    print("Ringkasan:", ringkasan)
    print("Modul processing berfungsi normal.")

