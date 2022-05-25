from django.shortcuts import render

# Create your views here.
from django.db import connection
from collections import namedtuple

def menu_aset(request):
    return render(request, 'menu_aset.html', {'role': request.session.get('role')})

def tuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def read(request):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""select * from aset;""")
        hasil = tuplefetchall(c)

    response = {'hasil': hasil,}

    return render(request, 'aset.html', response)

def read_dekorasi(request):
    if request.session.get('role') == "admin" or request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select d.id_aset, a.nama, a.minimum_level, a.harga_beli, d.harga_jual 
            from dekorasi d, aset a
            where a.id = d.id_aset;
            """)
            hasil = tuplefetchall(c)
    if request.session.get('role') == "admin":
        response = {'hasil': hasil, 'role': 'admin'} 
        return render(request, 'lihat_dekorasi.html', response)
    else:
        response = {'hasil': hasil, 'role': 'pengguna'} 
        return render(request, 'lihat_dekorasi.html', response)
    
    response = {'hasil': hasil}
    return render(request, 'lihat_dekorasi.html', response)

def read_bibit(request):
    if request.session.get('role') == "admin" or request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select b.id_aset, a.nama, a.minimum_level, a.harga_beli, b.durasi_panen 
            from bibit_tanaman b, aset a
            where a.id = b.id_aset;
            """)
            hasil = tuplefetchall(c)
    if request.session.get('role') == "admin":
        response = {'hasil': hasil, 'role': 'admin'} 
        return render(request, 'lihat_bibit_tanaman.html', response)
    else:
        response = {'hasil': hasil, 'role': 'pengguna'} 
        return render(request, 'lihat_bibit_tanaman.html', response)

    response = {'hasil': hasil,}
    return render(request, 'lihat_bibit_tanaman.html', response)

def read_kandang(request):
    if request.session.get('role') == "admin" or request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select k.id_aset, a.nama, a.minimum_level, a.harga_beli, k.kapasitas_maks, k.jenis_hewan
            from kandang k, aset a
            where a.id = k.id_aset;
            """)
            hasil = tuplefetchall(c)
    if request.session.get('role') == "admin":
        response = {'hasil': hasil, 'role': 'admin'} 
        return render(request, 'lihat_kandang.html', response)
    else:
        response = {'hasil': hasil, 'role': 'pengguna'} 
        return render(request, 'lihat_kandang.html', response)

    response = {'hasil': hasil,}
    return render(request, 'lihat_kandang.html', response)

def read_hewan(request):
    if request.session.get('role') == "admin" or request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select h.id_aset, a.nama, a.minimum_level, a.harga_beli, h.durasi_produksi, h.id_kandang 
            from hewan h, aset a
            where a.id = h.id_aset;
            """)
            hasil = tuplefetchall(c)
    if request.session.get('role') == "admin":
        response = {'hasil': hasil, 'role': 'admin'} 
        return render(request, 'lihat_hewan.html', response)
    else:
        response = {'hasil': hasil, 'role': 'pengguna'} 
        return render(request, 'lihat_hewan.html', response)

    response = {'hasil': hasil,}
    return render(request, 'lihat_hewan.html', response)

def read_alatproduksi(request):
    if request.session.get('role') == "admin" or request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select p.id_aset, a.nama, a.minimum_level, a.harga_beli, p.kapasitas_maks 
            from alat_produksi p, aset a
            where a.id = p.id_aset;
            """)
            hasil = tuplefetchall(c)
    if request.session.get('role') == "admin":
        response = {'hasil': hasil, 'role': 'admin'} 
        return render(request, 'lihat_alatproduksi.html', response)
    else:
        response = {'hasil': hasil, 'role': 'pengguna'} 
        return render(request, 'lihat_alatproduksi.html', response)
        
    response = {'hasil': hasil,}
    return render(request, 'lihat_alatproduksi.html', response)

def read_petak(request):
    if request.session.get('role') == "admin" or request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select p.id_aset, a.nama, a.minimum_level, a.harga_beli, p.jenis_tanaman
            from petak_sawah p, aset a
            where a.id = p.id_aset;
            """)
            hasil = tuplefetchall(c)
    if request.session.get('role') == "admin":
        response = {'hasil': hasil, 'role': 'admin'} 
        return render(request, 'lihat_petak_sawah.html', response)
    else:
        response = {'hasil': hasil, 'role': 'pengguna'} 
        return render(request, 'lihat_petak_sawah.html', response)
            
    response = {'hasil': hasil,}
    return render(request, 'lihat_petak_sawah.html', response)

def isAdmin(request):
    if request.session.get('role') == "admin":
        return True
    else:
        return False;
