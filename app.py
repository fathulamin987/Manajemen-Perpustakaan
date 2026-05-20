from flask import Flask, render_template, request, redirect
import json
import os

# =========================
# IMPORT ADT / STRUKTUR DATA
# =========================
from struktur_data.binary_tree_buku import BinaryTree
from struktur_data.hashing_buku import HashingBuku
from struktur_data.pencarian import cari_buku
from struktur_data.pengurutan import urutkan_judul
from struktur_data.stack_riwayat import StackRiwayat

app = Flask(__name__)

# HELPER JSON
def baca_json(path):

    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def simpan_json(path, data):

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# DASHBOARD
@app.route("/")
def dashboard():

    buku = baca_json("data/data_buku.json")
    mahasiswa = baca_json("data/data_mahasiswa.json")
    peminjaman = baca_json("data/data_peminjaman.json")

    return render_template(
        "dashboard.html",
        total_buku=len(buku),
        total_mahasiswa=len(mahasiswa),
        total_peminjaman=len(peminjaman)
    )

# HALAMAN BUKU 
@app.route("/buku")
def buku():
    data_buku = baca_json("data/data_buku.json")

    # TANGKAP INPUT KEYWORD & KATEGORI DARI HTML
    keyword = request.args.get("keyword", "")
    kategori_terpilih = request.args.get("kategori", "")

    # PROSES SEARCHING ADT (JIKA ADA KEYWORD)
    if keyword:
        data_buku = cari_buku(data_buku, keyword)

    # BINARY TREE ADT
    tree = BinaryTree()
    for item in data_buku:
        tree.insert(item)

    # SORTING ADT (Mengambil hasil urutan dari BinaryTree)
    data_buku = urutkan_judul(tree.inorder())

    # PROSES FILTER KATEGORI (Dilakukan paling akhir agar tidak tertimpa struktur Tree)
    if kategori_terpilih:
        data_buku = [buku for buku in data_buku if buku.get("kategori") == kategori_terpilih]

    # KIRIMKAN VARIABEL KE HTML
    return render_template(
        "buku.html",
        buku=data_buku,
        keyword=keyword,
        kategori_terpilih=kategori_terpilih
    )

# TAMBAH BUKU
@app.route("/tambah_buku", methods=["POST"])
def tambah_buku():

    data_buku = baca_json("data/data_buku.json")

    buku_baru = {
        "kode": request.form["kode"],
        "judul": request.form["judul"],
        "penulis": request.form["penulis"],
        "stok": int(request.form["stok"]),
        "kategori": request.form["kategori"]
    }

    data_buku.append(buku_baru)

    simpan_json("data/data_buku.json", data_buku)

    return redirect("/buku")


# =========================
# EDIT BUKU
# MENGGUNAKAN HASHING
# =========================
@app.route("/edit_buku/<kode>")
def edit_buku(kode):

    data_buku = baca_json("data/data_buku.json")

    hashing = HashingBuku()

    for buku in data_buku:
        hashing.tambah(buku["kode"], buku)

    buku_edit = hashing.cari(kode)

    return render_template(
        "edit_buku.html",
        buku=buku_edit
    )


# UPDATE BUKU
@app.route("/update_buku/<kode>", methods=["POST"])
def update_buku(kode):

    data_buku = baca_json("data/data_buku.json")

    for item in data_buku:

        if item["kode"] == kode:

            item["judul"] = request.form["judul"]
            item["penulis"] = request.form["penulis"]
            item["stok"] = int(request.form["stok"])
            item["kategori"] = request.form["kategori"]

            break

    simpan_json("data/data_buku.json", data_buku)

    return redirect("/buku")


# =========================
# HAPUS BUKU
# =========================
@app.route("/hapus_buku/<kode>")
def hapus_buku(kode):

    data_buku = baca_json("data/data_buku.json")

    data_baru = []

    for item in data_buku:

        if item["kode"] != kode:
            data_baru.append(item)

    simpan_json("data/data_buku.json", data_baru)

    return redirect("/buku")


# =========================
# CARI BERDASARKAN KODE
# MENGGUNAKAN HASHING
# =========================
@app.route("/cari_kode")
def cari_kode():

    kode = request.args.get("kode", "")

    data_buku = baca_json("data/data_buku.json")

    hashing = HashingBuku()

    for buku in data_buku:
        hashing.tambah(buku["kode"], buku)

    hasil = hashing.cari(kode)

    return render_template(
        "buku.html",
        hasil=hasil
    )


# =========================
# HALAMAN MAHASISWA
# =========================
@app.route("/mahasiswa")
def mahasiswa():

    data_mahasiswa = baca_json("data/data_mahasiswa.json")

    return render_template(
        "mahasiswa.html",
        mahasiswa=data_mahasiswa
    )


# =========================
# TAMBAH MAHASISWA
# =========================
@app.route("/tambah_mahasiswa", methods=["POST"])
def tambah_mahasiswa():

    data_mahasiswa = baca_json("data/data_mahasiswa.json")

    mahasiswa_baru = {
        "nim": request.form["nim"],
        "nama": request.form["nama"],
        "prodi": request.form["prodi"]
    }

    data_mahasiswa.append(mahasiswa_baru)

    simpan_json("data/data_mahasiswa.json", data_mahasiswa)

    return redirect("/mahasiswa")

# =========================
# HAPUS MAHASISWA
# =========================
@app.route("/hapus_mahasiswa/<nim>")
def hapus_mahasiswa(nim):

    data_mahasiswa = baca_json("data/data_mahasiswa.json")

    data_baru = []

    for item in data_mahasiswa:

        if item["nim"] != nim:
            data_baru.append(item)

    simpan_json("data/data_mahasiswa.json", data_baru)

    return redirect("/mahasiswa")


# =========================
# HALAMAN PEMINJAMAN
# =========================
@app.route("/peminjaman")
def peminjaman():

    buku = baca_json("data/data_buku.json")
    mahasiswa = baca_json("data/data_mahasiswa.json")
    peminjaman = baca_json("data/data_peminjaman.json")

    return render_template(
        "peminjaman.html",
        buku=buku,
        mahasiswa=mahasiswa,
        peminjaman=peminjaman
    )


# =========================
# TAMBAH PEMINJAMAN
# =========================
@app.route("/tambah_peminjaman", methods=["POST"])
def tambah_peminjaman():

    data_peminjaman = baca_json("data/data_peminjaman.json")

    pinjam_baru = {
        "nim": request.form["nim"],
        "kode_buku": request.form["kode_buku"],
        "durasi": int(request.form["durasi"])
    }

    data_peminjaman.append(pinjam_baru)

    simpan_json("data/data_peminjaman.json", data_peminjaman)

    return redirect("/peminjaman")


# =========================
# PENGEMBALIAN
# MENGGUNAKAN STACK
# =========================
@app.route("/pengembalian/<kode>")
def pengembalian(kode):

    data_peminjaman = baca_json("data/data_peminjaman.json")
    data_riwayat = baca_json("data/data_riwayat.json")

    stack = StackRiwayat()

    data_baru = []

    for item in data_peminjaman:

        if item["kode_buku"] == kode:

            # PUSH KE STACK
            stack.push(item)

        else:
            data_baru.append(item)

    # POP DARI STACK KE RIWAYAT
    while stack.tampilkan():

        data_riwayat.append(stack.pop())

    simpan_json("data/data_peminjaman.json", data_baru)
    simpan_json("data/data_riwayat.json", data_riwayat)

    return redirect("/peminjaman")


# =========================
# HALAMAN RIWAYAT
# =========================
@app.route("/riwayat")
def riwayat():

    data_riwayat = baca_json("data/data_riwayat.json")

    return render_template(
        "riwayat.html",
        riwayat=data_riwayat
    )


# =========================
# MENJALANKAN FLASK
# =========================
if __name__ == "__main__":
    app.run(debug=True)