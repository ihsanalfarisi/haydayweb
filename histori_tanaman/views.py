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
        c.execute("""select ht.email,ht.waktu_awal,hp.waktu_selesai,hp.jumlah, hp.xp, a.nama from histori_tanaman ht, histori_produksi hp, bibit_tanaman bt, aset a where ht.email = hp.email and ht.waktu_awal = hp.waktu_awal and ht.id_bibit_tanaman = bt.id_aset and bt.id_aset = a.id;""")
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil,}

    return render(request, 'histori_tanaman.html', response)