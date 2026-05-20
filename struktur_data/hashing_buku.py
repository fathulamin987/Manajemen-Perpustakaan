class HashingBuku:

    def __init__(self):
        self.data = {}

    def tambah(self, kode, buku):
        self.data[kode] = buku

    def cari(self, kode):
        return self.data.get(kode)