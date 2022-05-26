from django.shortcuts import render, redirect

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

def menu_buat(request):
    return render(request, 'menu_buat.html', {'role': request.session.get('role')})

def buat_dekorasi(request):
    if(request.method == "POST"):
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select * from dekorasi
            """)
            hasil = tuplefetchall(c)
        count = 0
        for aset in hasil:
            count+=1
        print(count)
        if count< 9:
            idauto = "d0{}".format(count+1)
        else:
            idauto = "d{}".format(count+1)
        print("masuk")
        buat = request.POST
        cursor = connection.cursor()
        id = idauto
        nama = buat['nama']
        minimum_level = buat['minimum_level']
        harga_beli = buat['harga_beli']
        harga_jual = buat['unik']
        print(id)

        buat = f"insert into hiday.aset values ('{id}', '{nama}', {minimum_level}, {harga_beli})"
        cursor.execute(buat)
        cursor.close()

        cursor = connection.cursor()

        buat = f"insert into hiday.dekorasi values ('{id}', {harga_jual})"
        cursor.execute(buat)
        cursor.close()

        return redirect('lihat_dekorasi')

    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""
        select * from dekorasi
        """)
        hasil = tuplefetchall(c)
    count = 0
    for aset in hasil:
        count+=1
    print(count)
    if count< 9:
        idauto = "d0{}".format(count+1)
    else:
        idauto = "d{}".format(count+1)
    response = {'role': 'admin', 'id': idauto, 'jenis': 'd'}
    return render(request, 'buat_aset.html', response)

def buat_bibit(request):
    if(request.method == "POST"):
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select * from bibit_tanaman 
            """)
            hasil = tuplefetchall(c)
        count = 0
        for aset in hasil:
            count+=1
        print(count)
        if count< 9:
            idauto = "bt0{}".format(count+1)
        else:
            idauto = "bt{}".format(count+1)
        print("masuk")
        buat = request.POST
        cursor = connection.cursor()
        id = idauto
        nama = buat['nama']
        minimum_level = buat['minimum_level']
        harga_beli = buat['harga_beli']
        durasi_panen = buat['unik']
        print(id)

        buat = f"insert into hiday.aset values ('{id}', '{nama}', {minimum_level}, {harga_beli})"
        cursor.execute(buat)
        cursor.close()

        cursor = connection.cursor()

        buat = f"insert into hiday.bibit_tanaman values ('{id}', '{durasi_panen}')"
        cursor.execute(buat)
        cursor.close()

        return redirect('lihat_bibit')

    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""
        select * from bibit_tanaman
        """)
        hasil = tuplefetchall(c)
    count = 0
    for aset in hasil:
        count+=1
    print(count)
    if count< 9:
        idauto = "bt0{}".format(count+1)
    else:
        idauto = "bt{}".format(count+1)
    response = {'role': 'admin', 'id': idauto, 'jenis': 'bt'}
    return render(request, 'buat_aset.html', response)

def buat_kandang(request):
    if(request.method == "POST"):
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select * from kandang
            """)
            hasil = tuplefetchall(c)
        count = 0
        for aset in hasil:
            count+=1
        print(count)
        if count< 9:
            idauto = "k0{}".format(count+1)
        else:
            idauto = "k{}".format(count+1)
        print("masuk")
        buat = request.POST
        cursor = connection.cursor()
        id = idauto
        nama = buat['nama']
        minimum_level = buat['minimum_level']
        harga_beli = buat['harga_beli']
        kapasitas = buat['unik1']
        jenis  = buat['unik2']
        print(id)

        buat = f"insert into hiday.aset values ('{id}', '{nama}', {minimum_level}, {harga_beli})"
        cursor.execute(buat)
        cursor.close()

        cursor = connection.cursor()

        buat = f"insert into hiday.kandang values ('{id}', {kapasitas}, '{jenis}')"
        cursor.execute(buat)
        cursor.close()

        return redirect('lihat_kandang')

    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""
        select * from kandang
        """)
        hasil = tuplefetchall(c)
    count = 0
    for aset in hasil:
        count+=1
    print(count)
    if count< 9:
        idauto = "k0{}".format(count+1)
    else:
        idauto = "k{}".format(count+1)
    response = {'role': 'admin', 'id': idauto, 'jenis': 'k'}
    return render(request, 'buat_aset.html', response)

def buat_hewan(request):
    if(request.method == "POST"):
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select * from hewan
            """)
            hasil = tuplefetchall(c)
        count = 0
        for aset in hasil:
            count+=1
        print(count)
        if count< 9:
            idauto = "h0{}".format(count+1)
        else:
            idauto = "h{}".format(count+1)
        print("masuk")
        buat = request.POST
        cursor = connection.cursor()
        id = idauto
        nama = buat['nama']
        minimum_level = buat['minimum_level']
        harga_beli = buat['harga_beli']
        durasi = buat['unik']
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute(f"""
            select k.id_aset from kandang k, aset a
            where k.jenis_hewan = '{nama}'
            """)
            hasil = tuplefetchall(c)
        for aset in hasil:
            id_kandang = aset.id_aset
        print(id_kandang)
        
        buat = f"insert into hiday.aset values ('{id}', '{nama}', {minimum_level}, {harga_beli})"
        cursor.execute(buat)
        cursor.close()

        cursor = connection.cursor()

        buat = f"insert into hiday.hewan values ('{id}', '{durasi}', '{id_kandang}')"
        cursor.execute(buat)
        cursor.close()

        return redirect('lihat_hewan')

    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""
        select * from hewan
        """)
        hasil = tuplefetchall(c)
    count = 0
    for aset in hasil:
        count+=1
    print(count)
    if count< 9:
        idauto = "h0{}".format(count+1)
    else:
        idauto = "h{}".format(count+1)
    response = {'role': 'admin', 'id': idauto, 'jenis': 'h'}
    return render(request, 'buat_aset.html', response)

def buat_alat(request):
    if(request.method == "POST"):
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select * from alat_produksi
            """)
            hasil = tuplefetchall(c)
        count = 0
        for aset in hasil:
            count+=1
        print(count)
        if count< 9:
            idauto = "ap0{}".format(count+1)
        else:
            idauto = "ap{}".format(count+1)
        print("masuk")
        buat = request.POST
        cursor = connection.cursor()
        id = idauto
        nama = buat['nama']
        minimum_level = buat['minimum_level']
        harga_beli = buat['harga_beli']
        kapasitas = buat['unik']
        
        buat = f"insert into hiday.aset values ('{id}', '{nama}', {minimum_level}, {harga_beli})"
        cursor.execute(buat)
        cursor.close()

        cursor = connection.cursor()

        buat = f"insert into hiday.alat_produksi values ('{id}', {kapasitas})"
        cursor.execute(buat)
        cursor.close()

        return redirect('lihat_alatproduksi')

    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""
        select * from alat_produksi
        """)
        hasil = tuplefetchall(c)
    count = 0
    for aset in hasil:
        count+=1
    print(count)
    if count< 9:
        idauto = "ap0{}".format(count+1)
    else:
        idauto = "ap{}".format(count+1)
    response = {'role': 'admin', 'id': idauto, 'jenis': 'ap'}
    return render(request, 'buat_aset.html', response)

def buat_petak(request):
    if(request.method == "POST"):
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select * from petak_sawah
            """)
            hasil = tuplefetchall(c)
        count = 0
        for aset in hasil:
            count+=1
        print(count)
        if count< 9:
            idauto = "ps0{}".format(count+1)
        else:
            idauto = "ps{}".format(count+1)
        print("masuk")
        buat = request.POST
        cursor = connection.cursor()
        id = idauto
        nama = buat['nama']
        minimum_level = buat['minimum_level']
        harga_beli = buat['harga_beli']
        jenis = buat['unik']
        
        buat = f"insert into hiday.aset values ('{id}', '{nama}', {minimum_level}, {harga_beli})"
        cursor.execute(buat)
        cursor.close()

        cursor = connection.cursor()

        buat = f"insert into hiday.petak_sawah values ('{id}', '{jenis}')"
        cursor.execute(buat)
        cursor.close()

        return redirect('lihat_petaksawah')

    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""
        select * from alat_produksi
        """)
        hasil = tuplefetchall(c)
    count = 0
    for aset in hasil:
        count+=1
    print(count)
    if count< 9:
        idauto = "ps0{}".format(count+1)
    else:
        idauto = "ps{}".format(count+1)
    
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""
        select a.nama from aset a, bibit_tanaman bt
        where a.id = bt.id_aset
        """)
        hasil = tuplefetchall(c)

    response = {'role': 'admin', 'id': idauto, 'jenis': 'ps', 'hasil': hasil}
    return render(request, 'buat_aset.html', response)