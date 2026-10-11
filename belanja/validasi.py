def validasi_nama(nama):
    if not isinstance(nama, str) or not nama.strip():
        raise ValueError("Nama barang tidak boleh kosong.")
    return nama.strip()


def validasi_jumlah(jumlah):
    try:
        nilai = int(jumlah)
    except (ValueError, TypeError):
        raise ValueError("Jumlah barang harus berupa bilangan bulat.")

    if nilai <= 0:
        raise ValueError("Jumlah barang harus lebih besar dari 0.")
    return nilai


def validasi_satuan(satuan):
    if not isinstance(satuan, str) or not satuan.strip():
        raise ValueError("Satuan barang tidak boleh kosong.")
    return satuan.strip()


def validasi_id_ada(id_barang, daftar_barang):
    try:
        id_target = int(id_barang)
    except (ValueError, TypeError):
        raise ValueError("ID barang harus berupa bilangan bulat.")

    for barang in daftar_barang:
        if barang.id_barang == id_target:
            return barang

    raise ValueError(f"Barang dengan ID {id_target} tidak ditemukan dalam daftar belanja.")

