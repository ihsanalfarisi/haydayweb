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
        c.execute("""select pksi.id_alat_produksi, pksi.durasi, pksi.jumlah_unit_hasil, pksi.id_produk_makanan, a.id as idaset, a.nama as anama, pk.id as idproduk, pk.nama as pnama
                    from produksi as pksi 
                    join produk as pk
                    on pksi.id_produk_makanan = pk.id
                    join aset as a
                    on pksi.id_alat_produksi = a.id
                    where pksi.jumlah_unit_hasil is not null;
                    """)
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil,}

    return render(request, 'produksi.html', response)

def readadmin(request):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""select pksi.id_alat_produksi, pksi.durasi, pksi.jumlah_unit_hasil, pksi.id_produk_makanan, a.id as idaset, a.nama as anama, pk.id as idproduk, pk.nama as pnama
                    from produksi as pksi 
                    join produk as pk
                    on pksi.id_produk_makanan = pk.id
                    join aset as a
                    on pksi.id_alat_produksi = a.id
                    where pksi.jumlah_unit_hasil is not null;
                    """)
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil,}

    return render(request, 'produksi_admin.html', response)