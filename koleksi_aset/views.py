from django.shortcuts import render

# Create your views here.
from django.db import connection
from collections import namedtuple

def menu_koleksi(request):
    return render(request, 'menu_koleksi.html')

def tuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def read(request):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""select * from koleksi_aset_memiliki_aset;""")
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil,}

    return render(request, 'koleksi_aset.html', response)

def read_dekorasi(request):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""select * from aset a, koleksi_aset_memiliki_aset ka, dekorasi d where d.id_aset = a.id and a.id=ka.id_aset;
        """)
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil,}

    return render(request, 'lihat_dekorasi.html', response)

def read_bibit(request):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""select b.id_aset, a.nama, a.minimum_level, a.harga_beli, b.durasi_panen 
        from bibit_tanaman b, aset a
        where a.id = b.id_aset;
        """)
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil,}

    return render(request, 'lihat_bibit_tanaman.html', response)

def read_kandang(request):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""select k.id_aset, a.nama, a.minimum_level, a.harga_beli, k.kapasitas_maks, k.jenis_hewan
        from kandang k, aset a
        where a.id = k.id_aset;
        """)
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil,}

    return render(request, 'lihat_kandang.html', response)

def read_hewan(request):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""select h.id_aset, a.nama, a.minimum_level, a.harga_beli, h.durasi_produksi, h.id_kandang 
        from hewan h, aset a
        where a.id = h.id_aset;
        """)
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil,}

    return render(request, 'lihat_hewan.html', response)

def read_alatproduksi(request):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""select p.id_aset, a.nama, a.minimum_level, a.harga_beli, p.kapasitas_maks 
        from alat_produksi p, aset a
        where a.id = p.id_aset;
        """)
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil,}

    return render(request, 'lihat_alatproduksi.html', response)

def read_petak(request):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""select p.id_aset, a.nama, a.minimum_level, a.harga_beli, p.jenis_tanaman
        from petak_sawah p, aset a
        where a.id = p.id_aset;
        """)
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil,}

    return render(request, 'lihat_petak_sawah.html', response)
