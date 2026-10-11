class Barang:
    def __init__(self, id_barang, nama, jumlah, satuan, status="Belum Dibeli", **kwargs):
        self.id_barang = int(id_barang)
        self.nama = str(nama).strip()
        self.jumlah = int(jumlah)
        self.satuan = str(satuan).strip()
        self.status = str(status).strip()
        # Menggunakan kwargs untuk menerima atribut opsional seperti catatan
        self.catatan = kwargs.get("catatan", "")

    def ubah_status(self, status_baru):
        status_valid = ["Belum Dibeli", "Sudah Dibeli"]
        if status_baru not in status_valid:
            raise ValueError(f"Status tidak valid. Pilihan: {', '.join(status_valid)}")
        self.status = status_baru

    def tandai_sudah_dibeli(self):
        self.status = "Sudah Dibeli"

    def tandai_belum_dibeli(self):
        self.status = "Belum Dibeli"

    def to_line(self):
        # Format penyimpanan teks: id|nama|jumlah|satuan|status|catatan
        return f"{self.id_barang}|{self.nama}|{self.jumlah}|{self.satuan}|{self.status}|{self.catatan}\n"

    def __str__(self):
        catatan_info = f" ({self.catatan})" if self.catatan else ""
        return f"[{self.id_barang}] {self.nama} - {self.jumlah} {self.satuan} [{self.status}]{catatan_info}"

