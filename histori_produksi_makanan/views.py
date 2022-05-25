from django.shortcuts import render

# Create your views here.
from django.db import connection
from collections import namedtuple

def tuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def read(request):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""select hpm.email, hpm.waktu_awal, hp.waktu_selesai, hpm.id_produk_makanan, 
                    hp.jumlah, hp.xp, pk.nama as pnama, a.nama as anama
                    from histori_produksi_makanan as hpm
                    join histori_produksi as hp
                    on hpm.email = hp.email
                    join produk as pk
                    on hpm.id_produk_makanan = pk.id
                    join aset as a
                    on hpm.id_alat_produksi = a.id""")
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil,}

    return render(request, 'histori_produksi_makanan.html', response)