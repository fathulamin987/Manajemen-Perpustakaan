def cari_buku(data_buku, keyword):

    hasil = []

    for buku in data_buku:

        if keyword.lower() in buku["judul"].lower():
            hasil.append(buku)

    return hasil