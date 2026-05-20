def urutkan_judul(data_buku):

    n = len(data_buku)

    for i in range(n):

        for j in range(0, n - i - 1):

            if data_buku[j]["judul"] > data_buku[j + 1]["judul"]:

                sementara = data_buku[j]

                data_buku[j] = data_buku[j + 1]

                data_buku[j + 1] = sementara

    return data_buku