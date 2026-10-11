from belanja.fileio import (
    inisialisasi_file,
    baca_data,
    tambah_ke_file,
    simpan_semua,
    tulis_laporan,
)
from belanja.processing import (
    tambah_barang,
    cari_barang,
    urutkan_barang,
    ubah_status_barang,
    hapus_barang,
    hitung_ringkasan,
    format_baris_tabel,
    buat_teks_laporan,
)

# Nama file penyimpanan data dan laporan
FILE_DATA = "data_belanja.txt"
FILE_LAPORAN = "laporan_belanja.txt"


def tampilkan_header():
    print("=" * 40)
    print("        APLIKASI DAFTAR BELANJA")
    print("=" * 40)
    print("1. Tambah barang")
    print("2. Tampilkan daftar belanja")
    print("3. Cari barang")
    print("4. Ubah status pembelian")
    print("5. Hapus barang")
    print("6. Urutkan berdasarkan nama")
    print("7. Lihat ringkasan")
    print("8. Buat laporan")
    print("0. Keluar")
    print("=" * 40)


def tampilkan_tabel_barang(daftar_barang):
    if not daftar_barang:
        print("\n[INFO] Daftar belanja masih kosong.")
        return

    garis = "-" * 75
    print("\n" + garis)
    print(format_baris_tabel("ID", "Nama Barang", "Jumlah", "Satuan", "Status", "Catatan"))
    print(garis)
    for b in daftar_barang:
        print(format_baris_tabel(b.id_barang, b.nama, b.jumlah, b.satuan, b.status, b.catatan))
    print(garis)


def menu_tambah_barang(daftar_barang):
    print("\n--- TAMBAH BARANG BARU ---")
    nama = input("Masukkan nama barang   : ")
    jumlah = input("Masukkan jumlah barang : ")
    satuan = input("Masukkan satuan barang : ")
    catatan = input("Catatan tambahan (opsional) : ").strip()

    try:
        # Memanggil fungsi menggunakan keyword arguments
        barang_baru = tambah_barang(
            daftar_barang=daftar_barang,
            nama=nama,
            jumlah=jumlah,
            satuan=satuan,
            catatan=catatan
        )
        # Menambahkan langsung ke file data (mode append 'a')
        tambah_ke_file(nama_file=FILE_DATA, barang=barang_baru)
        print(f"[BERHASIL] Barang '{barang_baru.nama}' berhasil ditambahkan dengan ID {barang_baru.id_barang}.")
    except ValueError as e:
        print(f"[GAGAL] {e}")


def menu_tampilkan_barang(daftar_barang):
    print("\n--- DAFTAR BELANJA LENGKAP ---")
    tampilkan_tabel_barang(daftar_barang)


def menu_cari_barang(daftar_barang):
    print("\n--- CARI BARANG ---")
    kata_kunci = input("Masukkan nama barang yang dicari: ").strip()
    if not kata_kunci:
        print("[PERINGATAN] Kata kunci pencarian tidak boleh kosong.")
        return

    hasil = cari_barang(daftar_barang=daftar_barang, kata_kunci=kata_kunci)
    if hasil:
        print(f"\nDitemukan {len(hasil)} barang yang cocok:")
        tampilkan_tabel_barang(hasil)
    else:
        print(f"\n[INFO] Barang dengan kata kunci '{kata_kunci}' tidak ditemukan.")


def menu_ubah_status(daftar_barang):
    print("\n--- UBAH STATUS PEMBELIAN ---")
    if not daftar_barang:
        print("[INFO] Daftar belanja masih kosong.")
        return

    tampilkan_tabel_barang(daftar_barang)
    id_input = input("Masukkan ID barang yang ingin diubah statusnya: ")

    try:
        id_barang = int(id_input)
        print("\nPilih status baru:")
        print("1. Sudah Dibeli")
        print("2. Belum Dibeli")
        print("3. Beralih otomatis (Toggle)")
        pilihan = input("Pilih opsi (1/2/3): ").strip()

        status_target = None
        if pilihan == "1":
            status_target = "Sudah Dibeli"
        elif pilihan == "2":
            status_target = "Belum Dibeli"
        elif pilihan == "3":
            status_target = None
        else:
            print("[GAGAL] Pilihan opsi status tidak valid.")
            return

        barang = ubah_status_barang(daftar_barang=daftar_barang, id_barang=id_barang, status_baru=status_target)
        # Simpan pembaruan status ke file (mode overwrite 'w')
        simpan_semua(nama_file=FILE_DATA, daftar_barang=daftar_barang)
        print(f"[BERHASIL] Status barang '{barang.nama}' diubah menjadi '{barang.status}'.")
    except ValueError as e:
        print(f"[GAGAL] {e}")


def menu_hapus_barang(daftar_barang):
    print("\n--- HAPUS BARANG ---")
    if not daftar_barang:
        print("[INFO] Daftar belanja masih kosong.")
        return

    tampilkan_tabel_barang(daftar_barang)
    id_input = input("Masukkan ID barang yang ingin dihapus: ")

    try:
        id_barang = int(id_input)
        konfirmasi = input(f"Yakin ingin menghapus barang dengan ID {id_barang}? (y/n): ").strip().lower()
        if konfirmasi == "y":
            barang_dihapus = hapus_barang(daftar_barang=daftar_barang, id_barang=id_barang)
            # Simpan perubahan daftar setelah penghapusan ke file
            simpan_semua(nama_file=FILE_DATA, daftar_barang=daftar_barang)
            print(f"[BERHASIL] Barang '{barang_dihapus.nama}' berhasil dihapus.")
        else:
            print("[INFO] Penghapusan barang dibatalkan.")
    except ValueError as e:
        print(f"[GAGAL] {e}")


def menu_urutkan_barang(daftar_barang):
    print("\n--- URUTKAN BERDASARKAN NAMA (A-Z) ---")
    if not daftar_barang:
        print("[INFO] Daftar belanja masih kosong.")
        return

    daftar_terurut = urutkan_barang(daftar_barang=daftar_barang, reverse=False)
    tampilkan_tabel_barang(daftar_terurut)

    simpan = input("Simpan urutan ini secara permanen ke file data? (y/n): ").strip().lower()
    if simpan == "y":
        daftar_barang.clear()
        daftar_barang.extend(daftar_terurut)
        simpan_semua(nama_file=FILE_DATA, daftar_barang=daftar_barang)
        print("[BERHASIL] Urutan daftar barang telah diperbarui ke file data.")


def menu_ringkasan(daftar_barang):
    print("\n--- RINGKASAN DAFTAR BELANJA ---")
    ringkasan = hitung_ringkasan(daftar_barang=daftar_barang)
    print(f"Total Barang          : {ringkasan['total']}")
    print(f"Barang Sudah Dibeli   : {ringkasan['sudah']}")
    print(f"Barang Belum Dibeli   : {ringkasan['belum']}")
    print(f"Persentase Selesai    : {ringkasan['persentase']}%")


def menu_buat_laporan(daftar_barang):
    print("\n--- BUAT LAPORAN KE FILE ---")
    ringkasan = hitung_ringkasan(daftar_barang=daftar_barang)
    teks = buat_teks_laporan(daftar_barang=daftar_barang, ringkasan=ringkasan)

    tulis_laporan(nama_file=FILE_LAPORAN, isi_laporan=teks)
    print(f"[BERHASIL] Laporan berhasil dibuat dan disimpan di '{FILE_LAPORAN}'.")


def main():
    # Pastikan file data tersedia saat program pertama kali dibuka
    inisialisasi_file(FILE_DATA)
    daftar_belanja = baca_data(FILE_DATA)

    while True:
        tampilkan_header()
        pilihan = input("\nPilih menu: ").strip()

        if pilihan == "1":
            menu_tambah_barang(daftar_belanja)
        elif pilihan == "2":
            menu_tampilkan_barang(daftar_belanja)
        elif pilihan == "3":
            menu_cari_barang(daftar_belanja)
        elif pilihan == "4":
            menu_ubah_status(daftar_belanja)
        elif pilihan == "5":
            menu_hapus_barang(daftar_belanja)
        elif pilihan == "6":
            menu_urutkan_barang(daftar_belanja)
        elif pilihan == "7":
            menu_ringkasan(daftar_belanja)
        elif pilihan == "8":
            menu_buat_laporan(daftar_belanja)
        elif pilihan == "0":
            print("\nTerima kasih telah menggunakan Aplikasi Daftar Belanja. Sampai jumpa!")
            break
        else:
            print("\n[PERINGATAN] Menu tidak valid. Silakan masukkan angka dari 0 sampai 8.")

        input("\nTekan Enter untuk melanjutkan...")


if __name__ == "__main__":
    main()

