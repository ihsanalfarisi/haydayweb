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
    role =""
    if request.session.get('role') == "admin":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select km.id_koleksi_aset, a.nama, a.minimum_level, a.harga_beli, km.jumlah
            FROM KOLEKSI_ASET_MEMILIKI_ASET km, aset a, koleksi_aset ka, dekorasi d
            WHERE
            km.id_aset = a.id and
            ka.email = km.id_koleksi_aset and
            a.id = d.id_aset;   
            """)
            hasil = tuplefetchall(c)
            role = "admin"

    elif request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select a.nama, a.minimum_level, a.harga_beli, km.jumlah
            FROM KOLEKSI_ASET_MEMILIKI_ASET km, aset a, koleksi_aset ka, dekorasi d
            WHERE
            km.id_aset = a.id and
            ka.email = km.id_koleksi_aset and
            a.id = d.id_aset and
            email = '{}';""".format(request.session.get('email'))) 
            hasil = tuplefetchall(c)
            role = "pengguna"
    
    response = {'hasil': hasil, 'role': role}

    return render(request, 'lihat_kdekorasi.html', response)

def read_bibit(request):
    role =""
    if request.session.get('role') == "admin":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select km.id_koleksi_aset, a.nama, a.minimum_level, a.harga_beli, km.jumlah
            FROM KOLEKSI_ASET_MEMILIKI_ASET km, aset a, koleksi_aset ka, bibit_tanaman bt
            WHERE
            km.id_aset = a.id and
            ka.email = km.id_koleksi_aset and
            a.id = bt.id_aset;
            """)
            hasil = tuplefetchall(c)
            role = "admin"
    
    elif request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select a.nama, a.minimum_level, a.harga_beli, km.jumlah
            FROM KOLEKSI_ASET_MEMILIKI_ASET km, aset a, koleksi_aset ka, bibit_tanaman bt
            WHERE
            km.id_aset = a.id and
            ka.email = km.id_koleksi_aset and
            a.id = bt.id_aset and
            email = '{}';""".format(request.session.get('email')))
            hasil = tuplefetchall(c)
            role = "pengguna"
    
    response = {'hasil': hasil, 'role': role}
    
    return render(request, 'lihat_kbibit_tanaman.html', response)

def read_kandang(request):
    role =""
    if request.session.get('role') == "admin":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select km.id_koleksi_aset, a.nama, a.minimum_level, a.harga_beli, km.jumlah
            FROM KOLEKSI_ASET_MEMILIKI_ASET km, aset a, koleksi_aset ka, kandang k
            WHERE
            km.id_aset = a.id and
            ka.email = km.id_koleksi_aset and
            a.id = k.id_aset;
            """)
            hasil = tuplefetchall(c)
            role = "admin"
    
    elif request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select a.nama, a.minimum_level, a.harga_beli, km.jumlah
            FROM KOLEKSI_ASET_MEMILIKI_ASET km, aset a, koleksi_aset ka, kandang k
            WHERE
            km.id_aset = a.id and
            ka.email = km.id_koleksi_aset and
            a.id = k.id_aset and
            email = '{}';""".format(request.session.get('email')))
            hasil = tuplefetchall(c)
            role = "pengguna"
    
    response = {'hasil': hasil, 'role': role}

    return render(request, 'lihat_kkandang.html', response)

def read_hewan(request):
    role = ""
    if request.session.get('role') == "admin":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select km.id_koleksi_aset, a.nama, a.minimum_level, a.harga_beli, km.jumlah
            FROM KOLEKSI_ASET_MEMILIKI_ASET km, aset a, koleksi_aset ka, hewan h
            WHERE
            km.id_aset = a.id and
            ka.email = km.id_koleksi_aset and
            a.id = h.id_aset;
            """)
            hasil = tuplefetchall(c)
            role = "admin"
    
    elif request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select a.nama, a.minimum_level, a.harga_beli, km.jumlah
            FROM KOLEKSI_ASET_MEMILIKI_ASET km, aset a, koleksi_aset ka, hewan h
            WHERE
            km.id_aset = a.id and
            ka.email = km.id_koleksi_aset and
            a.id = h.id_aset and
            email = '{}';""".format(request.session.get('email')))
            hasil = tuplefetchall(c)
            role = "pengguna"
    
    response = {'hasil': hasil, 'role': role}

    return render(request, 'lihat_khewan.html', response)

def read_alatproduksi(request):
    role = ""
    if request.session.get('role') == "admin":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select km.id_koleksi_aset, a.nama, a.minimum_level, a.harga_beli, km.jumlah
            FROM KOLEKSI_ASET_MEMILIKI_ASET km, aset a, koleksi_aset ka, alat_produksi ap
            WHERE
            km.id_aset = a.id and
            ka.email = km.id_koleksi_aset and
            a.id = ap.id_aset;
            """)
            hasil = tuplefetchall(c)
            role = "admin"

    elif request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select km.id_koleksi_aset, a.nama, a.minimum_level, a.harga_beli, km.jumlah
            FROM KOLEKSI_ASET_MEMILIKI_ASET km, aset a, koleksi_aset ka, alat_produksi ap
            WHERE
            km.id_aset = a.id and
            ka.email = km.id_koleksi_aset and
            a.id = ap.id_aset and
            email = '{}';""".format(request.session.get('email')))
            hasil = tuplefetchall(c)
            role = "pengguna"
    
    response = {'hasil': hasil, 'role': role}

    return render(request, 'lihat_kalatproduksi.html', response)

def read_petak(request):
    role = ""
    if request.session.get('role') == "admin":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select km.id_koleksi_aset, a.nama, a.minimum_level, a.harga_beli, km.jumlah
            FROM KOLEKSI_ASET_MEMILIKI_ASET km, aset a, koleksi_aset ka, petak_sawah ps
            WHERE
            km.id_aset = a.id and
            ka.email = km.id_koleksi_aset and
            a.id = ps.id_aset;
            """)
            hasil = tuplefetchall(c)
            role = "admin"

    elif request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select km.id_koleksi_aset, a.nama, a.minimum_level, a.harga_beli, km.jumlah
            FROM KOLEKSI_ASET_MEMILIKI_ASET km, aset a, koleksi_aset ka, petak_sawah ps
            WHERE
            km.id_aset = a.id and
            ka.email = km.id_koleksi_aset and
            a.id = ps.id_aset and
            email = '{}';""".format(request.session.get('email')))
            hasil = tuplefetchall(c)
            role = "pengguna"

    response = {'hasil': hasil, 'role': role}

    return render(request, 'lihat_kpetak_sawah.html', response)
