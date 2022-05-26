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
    if request.session.get('role') == "admin":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select ht.email,ht.waktu_awal,hp.waktu_selesai,hp.jumlah, hp.xp, a.nama from histori_tanaman ht, histori_produksi hp, bibit_tanaman bt, aset a where ht.email = hp.email and ht.waktu_awal = hp.waktu_awal and ht.id_bibit_tanaman = bt.id_aset and bt.id_aset = a.id;""")
            hasil = tuplefetchall(c)
        
        response = {'hasil': hasil,}

        return render(request, 'histori_tanaman.html', response)
    elif request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("select ht.email,ht.waktu_awal,hp.waktu_selesai,hp.jumlah, hp.xp, a.nama from histori_tanaman ht, histori_produksi hp, bibit_tanaman bt, aset a where ht.email = hp.email and ht.waktu_awal = hp.waktu_awal and ht.id_bibit_tanaman = bt.id_aset and bt.id_aset = a.id and ht.email = '{}';".format(request.session.get('email')))
            hasil = tuplefetchall(c)
        
        response = {'hasil': hasil,}

        return render(request, 'histori_tanaman_peng.html', response)

def create_produksi(request):
    if request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("select a.nama from koleksi_aset_memiliki_aset kama, koleksi_aset ka, aset a where kama.id_koleksi_aset = ka.email and kama.id_aset = a.id and a.id like 'bt%' and ka.email = '{}';".format(request.session.get('email')))
            hasil = tuplefetchall(c)
        response = {'hasil': hasil}
        return render(request, 'create_produksi_tanaman.html', response)

def create_validation_produksi_tanaman(request):
    data_paket = {
        "jumlah_koin" : request.POST.get("jumlah_koin"),
        "harga" : request.POST.get("harga")
    }

    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""
        select jumlah_koin from paket_koin
        """)
        hasil = tuplefetchall(c)
        if len(data_paket['jumlah_koin'])==0:
            return render(request, 'create_paket_koin.html', {'message' : "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu"});
        if len(data_paket['harga'])==0:
            return render(request, 'create_paket_koin.html', {'message' : "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu"});
        for data in hasil :
            if str(data.jumlah_koin) == data_paket['jumlah_koin'] :
                return render(request, 'create_paket_koin.html', {'message' : "Data yang kamu masukkan sudah terdaftar di Database. Harap masukkan data lain"});
        jumlah_koinn= int(data_paket['jumlah_koin'])
        hargaa= int(data_paket['harga'])
        c.execute("insert into paket_koin values ('{}', '{}')".format(jumlah_koinn,hargaa))
    
        return redirect('/paket-koin/paket_koin/read')