from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)


def baca_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def simpan_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


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


@app.route("/buku")
def buku():
    data_buku = baca_json("data/data_buku.json")
    
    # Mengambil parameter filter_kategori dari dropdown filter di HTML
    filter_kategori = request.args.get("filter_kategori", "")
    
    # Jika kategori tertentu dipilih, lakukan penyaringan (filtering)
    if filter_kategori:
        data_buku = [item for item in data_buku if item.get("kategori") == filter_kategori]

    
    data_buku = sorted(data_buku, key=lambda x: x["judul"])

    return render_template(
        "buku.html", 
        buku=data_buku, 
        kategori_terpilih=filter_kategori
    )


@app.route("/tambah_buku", methods=["POST"])
def tambah_buku():
    data_buku = baca_json("data/data_buku.json")

    buku_baru = {
        "kode": request.form["kode"],
        "judul": request.form["judul"],
        "penulis": request.form["penulis"],
        "stok": int(request.form["stok"]),
        "kategori": request.form["kategori"]  # Menyimpan kategori dari form input
    }

    data_buku.append(buku_baru)
    simpan_json("data/data_buku.json", data_buku)
    return redirect("/buku")


@app.route("/edit_buku/<kode>")
def edit_buku(kode):
    data_buku = baca_json("data/data_buku.json")
    buku_edit = None

    for item in data_buku:
        if item["kode"] == kode:
            buku_edit = item
            break

    return render_template("edit_buku.html", buku=buku_edit)


@app.route("/update_buku/<kode>", methods=["POST"])
def update_buku(kode):
    data_buku = baca_json("data/data_buku.json")

    for item in data_buku:
        if item["kode"] == kode:
            item["judul"] = request.form["judul"]
            item["penulis"] = request.form["penulis"]
            item["stok"] = int(request.form["stok"])
            item["kategori"] = request.form["kategori"]  # Memperbarui kategori dari form edit
            break

    simpan_json("data/data_buku.json", data_buku)
    return redirect("/buku")


@app.route("/hapus_buku/<kode>")
def hapus_buku(kode):
    data_buku = baca_json("data/data_buku.json")
    data_baru = [item for item in data_buku if item["kode"] != kode]
    simpan_json("data/data_buku.json", data_baru)
    return redirect("/buku")


@app.route("/mahasiswa")
def mahasiswa():
    data_mahasiswa = baca_json("data/data_mahasiswa.json")
    return render_template("mahasiswa.html", mahasiswa=data_mahasiswa)


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


@app.route("/tambah_peminjaman", methods=["POST"])
def tambah_peminjaman():
    data_peminjaman = baca_json("data/data_peminjaman.json")

    pinjam_baru = {
        "nim": request.form["nim"],
        "kode_buku": request.form["kode_buku"]
    }

    data_peminjaman.append(pinjam_baru)
    simpan_json("data/data_peminjaman.json", data_peminjaman)
    return redirect("/peminjaman")


@app.route("/pengembalian/<kode>")
def pengembalian(kode):
    data_peminjaman = baca_json("data/data_peminjaman.json")
    data_riwayat = baca_json("data/data_riwayat.json")

    data_baru = []
    for item in data_peminjaman:
        if item["kode_buku"] == kode:
            data_riwayat.append(item)
        else:
            data_baru.append(item)

    simpan_json("data/data_peminjaman.json", data_baru)
    simpan_json("data/data_riwayat.json", data_riwayat)
    return redirect("/peminjaman")


@app.route("/riwayat")
def riwayat():
    data_riwayat = baca_json("data/data_riwayat.json")
    return render_template("riwayat.html", riwayat=data_riwayat)


if __name__ == "__main__":
    app.run(debug=True)