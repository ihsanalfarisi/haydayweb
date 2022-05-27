from urllib import response
from django.shortcuts import render, redirect
from django.contrib import messages

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
            c.execute("""
            select d.id_aset, a.nama, a.minimum_level, a.harga_beli, d.harga_jual, 
                CASE
                    WHEN NOT EXISTS (select * from koleksi_aset_memiliki_aset ka where d.id_aset = ka.id_aset) and 
                    NOT EXISTS (select * from transaksi_pembelian tp where d.id_aset = tp.id_aset) and
                    NOT EXISTS (select * from dekorasi_memiliki_histori_penjualan dm where d.id_aset = dm.id_dekorasi)
                    THEN 'y' ELSE 'n' END delete_
            from dekorasi d, aset a
            where a.id = d.id_aset
            order by id asc;
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
            c.execute("""
            select b.id_aset, a.nama, a.minimum_level, a.harga_beli, TO_CHAR(b.durasi_panen, 'HH24:MI:SS') durasi_panen,
                CASE
                    WHEN NOT EXISTS (select * from koleksi_aset_memiliki_aset ka where b.id_aset = ka.id_aset) and 
                    NOT EXISTS (select * from transaksi_pembelian tp where b.id_aset = tp.id_aset) and
                    NOT EXISTS (select * from histori_tanaman ht where b.id_aset = ht.id_bibit_tanaman) and
                    NOT EXISTS (select * from bibit_tanaman_ditanam_di_petak_sawah dps where b.id_aset = dps.id_bibit_tanaman) and
                    NOT EXISTS (select * from bibit_tanaman_menghasilkan_hasil_panen hp where b.id_aset = hp.id_bibit_tanaman)
                    THEN 'y' ELSE 'n' END delete_
            from bibit_tanaman b, aset a
            where a.id = b.id_aset
            order by id_aset asc;
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
            c.execute("""
            select k.id_aset, a.nama, a.minimum_level, a.harga_beli, k.kapasitas_maks, k.jenis_hewan,
                CASE
                    WHEN NOT EXISTS (select * from koleksi_aset_memiliki_aset ka where k.id_aset = ka.id_aset) and 
                    NOT EXISTS (select * from transaksi_pembelian tp where k.id_aset = tp.id_aset) and
                    NOT EXISTS (select * from hewan h where k.id_aset = h.id_kandang)
                    THEN 'y' ELSE 'n' END delete_
            from kandang k, aset a
            where a.id = k.id_aset
            order by id asc;
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
            c.execute("""
            select h.id_aset, a.nama, a.minimum_level, a.harga_beli, TO_CHAR(h.durasi_produksi, 'HH24:MI:SS') durasi_produksi, h.id_kandang,
                CASE
                    WHEN NOT EXISTS (select * from koleksi_aset_memiliki_aset ka where h.id_aset = ka.id_aset) and 
                    NOT EXISTS (select * from transaksi_pembelian tp where h.id_aset = tp.id_aset) and
                    NOT EXISTS (select * from histori_hewan hh where h.id_aset = hh.id_hewan) and
                    NOT EXISTS (select * from hewan_menghasilkan_produk_hewan hm where h.id_aset = hm.id_hewan)
                    THEN 'y' ELSE 'n' END delete_
            from hewan h, aset a
            where a.id = h.id_aset
            order by id asc;
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
            c.execute("""
            select p.id_aset, a.nama, a.minimum_level, a.harga_beli, p.kapasitas_maks,
                CASE
                    WHEN NOT EXISTS (select * from koleksi_aset_memiliki_aset ka where p.id_aset = ka.id_aset) and 
                    NOT EXISTS (select * from transaksi_pembelian tp where p.id_aset = tp.id_aset) and
                    NOT EXISTS (select * from produksi pr where p.id_aset = pr.id_alat_produksi)
                    THEN 'y' ELSE 'n' END delete_
            from alat_produksi p, aset a
            where a.id = p.id_aset
            order by id asc;
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
            c.execute("""
            select p.id_aset, a.nama, a.minimum_level, a.harga_beli, p.jenis_tanaman,
                CASE
                    WHEN NOT EXISTS (select * from koleksi_aset_memiliki_aset ka where p.id_aset = ka.id_aset) and 
                    NOT EXISTS (select * from transaksi_pembelian tp where p.id_aset = tp.id_aset) and
                    NOT EXISTS (select * from bibit_tanaman_ditanam_di_petak_sawah dps where p.id_aset = dps.id_bibit_tanaman)
                    THEN 'y' ELSE 'n' END delete_
            from petak_sawah p, aset a
            where a.id = p.id_aset
            order by id asc;
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

        if (minimum_level == '' or minimum_level == '' or harga_beli == '' or harga_jual == ''):
            messages.error(request,"Data belum lengkap, silakan lengkapi data terlebih dahulu.")

        else:  
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

        if (minimum_level == '' or minimum_level == '' or harga_beli == '' or durasi_panen == ''):
            messages.error(request,"Data belum lengkap, silakan lengkapi data terlebih dahulu.")

        else:  
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

        if (minimum_level == '' or minimum_level == '' or harga_beli == '' or kapasitas == '' or jenis == ''):
            messages.error(request,"Data belum lengkap, silakan lengkapi data terlebih dahulu.")

        else:  
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
        if hasil == []:
            messages.error(request,"Data kandang hewan tersebut belum ada, silakan dibuat.")
        else:
            for aset in hasil:
                id_kandang = aset.id_aset
            print(id_kandang)
            
            if (minimum_level == '' or minimum_level == '' or harga_beli == '' or durasi == ''):
                messages.error(request,"Data belum lengkap, silakan lengkapi data terlebih dahulu.")

            else:  
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
        
        if (minimum_level == '' or minimum_level == '' or harga_beli == '' or kapasitas == ''):
                messages.error(request,"Data belum lengkap, silakan lengkapi data terlebih dahulu.")

        else:  
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
            
        if (minimum_level == '' or minimum_level == '' or harga_beli == '' or jenis == ''):
                messages.error(request,"Data belum lengkap, silakan lengkapi data terlebih dahulu.")

        else:  
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

def update_dekorasi(request, id):
    role = 'admin'

    if(request.method == "POST"):
        update = request.POST
        cursor = connection.cursor()
        minimum_level = update['minimum_level']
        harga_beli = update['harga_beli']
        harga_jual = update['unik']
        
        if (minimum_level == '' or minimum_level == '' or harga_beli == '' or harga_jual == ''):
            messages.error(request,"Data belum lengkap, silakan lengkapi data terlebih dahulu.")

        else:    
            cursor.execute("""update hiday.aset set minimum_level = {}, harga_beli = {}
            where id = '{}'""".format(minimum_level, harga_beli, id))

            cursor.execute("""update hiday.dekorasi set harga_jual = '{}'
            where id_aset = {}""".format(harga_jual, id))

            return redirect('lihat_dekorasi')

    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""
        select a.id, a.nama, a.minimum_level, a.harga_beli, d.harga_jual from aset a, dekorasi d
        where a.id = d.id_aset and
        d.id_aset = '{}';""".format(id))
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil, 'role': role, 'jenis': 'd'}
    return render(request, 'update_aset.html', response)

def update_bibit(request, id):
    role = 'admin'

    if(request.method == "POST"):
        update = request.POST
        cursor = connection.cursor()
        minimum_level = update['minimum_level']
        harga_beli = update['harga_beli']
        durasi = update['unik']

        if (minimum_level == '' or minimum_level == '' or harga_beli == '' or durasi == ''):
            messages.error(request,"Data belum lengkap, silakan lengkapi data terlebih dahulu.")

        else:    
            cursor.execute("""update hiday.aset set minimum_level = {}, harga_beli = {}
            where id = '{}'""".format(minimum_level, harga_beli, id))

            cursor.execute("""update hiday.bibit_tanaman set durasi_panen = '{}'
            where id_aset = '{}'""".format(durasi, id))

            return redirect('lihat_bibit')

    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""
        select a.id, a.nama, a.minimum_level, a.harga_beli, bt.durasi_panen from aset a, bibit_tanaman bt
        where a.id = bt.id_aset and
        bt.id_aset = '{}';""".format(id))
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil, 'role': role, 'jenis': 'bt'}
    return render(request, 'update_aset.html', response)

def update_kandang(request, id):
    role = 'admin'

    if(request.method == "POST"):
        update = request.POST
        cursor = connection.cursor()
        minimum_level = update['minimum_level']
        harga_beli = update['harga_beli']
        kapasitas = update['unik']

        if (minimum_level == '' or minimum_level == '' or harga_beli == '' or kapasitas == ''):
            messages.error(request,"Data belum lengkap, silakan lengkapi data terlebih dahulu.")

        else:    
            cursor.execute("""update hiday.aset set minimum_level = {}, harga_beli = {}
            where id = '{}'""".format(minimum_level, harga_beli, id))

            cursor.execute("""update hiday.kandang set kapasitas_maks = '{}'
            where id_aset = '{}'""".format(kapasitas, id))

            return redirect('lihat_kandang')

    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""
        select a.id, a.nama, a.minimum_level, a.harga_beli, k.kapasitas_maks, k.jenis_hewan from aset a, kandang k
        where a.id = k.id_aset and
        k.id_aset = '{}';""".format(id))
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil, 'role': role, 'jenis': 'k'}
    return render(request, 'update_aset.html', response)

def update_hewan(request, id):
    role = 'admin'

    if(request.method == "POST"):
        update = request.POST
        cursor = connection.cursor()
        minimum_level = update['minimum_level']
        harga_beli = update['harga_beli']
        durasi = update['unik']

        if (minimum_level == '' or minimum_level == '' or harga_beli == '' or durasi == ''):
            messages.error(request,"Data belum lengkap, silakan lengkapi data terlebih dahulu.")

        else:    
            cursor.execute("""update hiday.aset set minimum_level = {}, harga_beli = {}
            where id = '{}'""".format(minimum_level, harga_beli, id))

            cursor.execute("""update hiday.hewan set durasi_produksi = '{}'
            where id_aset = '{}'""".format(durasi, id))

            return redirect('lihat_hewan')

    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""
        select a.id, a.nama, a.minimum_level, a.harga_beli, h.durasi_produksi, h.id_kandang from aset a, hewan h
        where a.id = h.id_aset and
        h.id_aset = '{}';""".format(id))
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil, 'role': role, 'jenis': 'h'}
    return render(request, 'update_aset.html', response)
    
def update_alat(request, id):
    role = 'admin'

    if(request.method == "POST"):
        update = request.POST
        cursor = connection.cursor()
        minimum_level = update['minimum_level']
        harga_beli = update['harga_beli']
        kapasitas = update['unik']

        if (minimum_level == '' or minimum_level == '' or harga_beli == '' or kapasitas == ''):
            messages.error(request,"Data belum lengkap, silakan lengkapi data terlebih dahulu.")

        else:    
            cursor.execute("""update hiday.aset set minimum_level = {}, harga_beli = {}
            where id = '{}'""".format(minimum_level, harga_beli, id))

            cursor.execute("""update hiday.alat_produksi set kapasitas_maks = '{}'
            where id_aset = '{}'""".format(kapasitas, id))

            return redirect('lihat_alatproduksi')

    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""
        select a.id, a.nama, a.minimum_level, a.harga_beli, ap.kapasitas_maks from aset a, alat_produksi ap
        where a.id = ap.id_aset and
        ap.id_aset = '{}';""".format(id))
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil, 'role': role, 'jenis': 'ap'}
    return render(request, 'update_aset.html', response)

def update_petak(request, id):
    role = 'admin'

    if(request.method == "POST"):
        update = request.POST
        cursor = connection.cursor()
        minimum_level = update['minimum_level']
        harga_beli = update['harga_beli']
        jenis = update['unik']

        if (minimum_level == '' or minimum_level == '' or harga_beli == '' or jenis == ''):
            messages.error(request,"Data belum lengkap, silakan lengkapi data terlebih dahulu.")

        else:    
            cursor.execute("""update hiday.aset set minimum_level = {}, harga_beli = {}
            where id = '{}'""".format(minimum_level, harga_beli, id))

            cursor.execute("""update hiday.petak_sawah set jenis_tanaman = '{}'
            where id_aset = '{}'""".format(jenis, id))

            return redirect('lihat_petaksawah')

    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""
        select a.id, a.nama, a.minimum_level, a.harga_beli, ps.jenis_tanaman from aset a, petak_sawah ps
        where a.id = ps.id_aset and
        ps.id_aset = '{}';""".format(id))
        hasil = tuplefetchall(c)
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""
        select a.nama from aset a, bibit_tanaman bt
        where a.id = bt.id_aset
        """)
        hasil2 = tuplefetchall(c)
    
    response = {'hasil': hasil, 'role': role, 'jenis': 'ps', 'hasil2': hasil2}
    return render(request, 'update_aset.html', response)

def delete_dekorasi(request, id):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("delete from dekorasi where id_aset = '{}'".format(id))

        c.execute("delete from aset where id = '{}'".format(id))
    
    return redirect('lihat_dekorasi')

def delete_bibit(request, id):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("delete from bibit_tanaman where id_aset = '{}'".format(id))

        c.execute("delete from aset where id = '{}'".format(id))
    
    return redirect('lihat_bibit')

def delete_kandang(request, id):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("delete from kandang where id_aset = '{}'".format(id))

        c.execute("delete from aset where id = '{}'".format(id))
    
    return redirect('lihat_kandang')

def delete_hewan(request, id):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("delete from hewan where id_aset = '{}'".format(id))

        c.execute("delete from aset where id = '{}'".format(id))
    
    return redirect('lihat_hewan')

def delete_alat(request, id):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("delete from alat_produksi where id_aset = '{}'".format(id))

        c.execute("delete from aset where id = '{}'".format(id))
    
    return redirect('lihat_alatproduksi')

def delete_petak(request, id):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("delete from petak_sawah where id_aset = '{}'".format(id))

        c.execute("delete from aset where id = '{}'".format(id))
    
    return redirect('lihat_petaksawah')
