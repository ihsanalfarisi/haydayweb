from urllib import response
from django.shortcuts import render, redirect

# Create your views here.
from django.db import connection
from collections import namedtuple

import datetime

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
    if request.session.get('role') == "pengguna":
        data_produksi = {
            "bibit" : request.POST.get("bibitTanaman"),
            "jumlah" : request.POST.get("jumlah"),
            "xp" : 5,
            "waktu" : datetime.datetime.now()
        }
        
        with connection.cursor() as c:
                c.execute("set search_path to hiday")
                c.execute("select a.nama from koleksi_aset_memiliki_aset kama, koleksi_aset ka, aset a where kama.id_koleksi_aset = ka.email and kama.id_aset = a.id and a.id like 'bt%' and ka.email = '{}';".format(request.session.get('email')))
                hasil = tuplefetchall(c)

        with connection.cursor() as c:
            if len(data_produksi['bibit'])==0:
                response = {'hasil' : hasil, 'message' : "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu"}
                return render(request, 'create_produksi_tanaman.html', response);
            if len(data_produksi['jumlah'])==0:
                response = {'hasil' : hasil, 'message' : "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu"}
                return render(request, 'create_produksi_tanaman.html', response);
            bibitt= data_produksi['bibit']
            jumlahh= int(data_produksi['jumlah'])
            data_produksi['xp'] = int(data_produksi['xp']) * jumlahh
            waktuu = data_produksi['waktu']
            xpp = int(data_produksi['xp'])
            c.execute("set search_path to hiday")
            c.execute("select kama.jumlah from koleksi_aset_memiliki_aset kama, aset a where kama.id_aset = a.id and kama.id_koleksi_aset = '{}' and a.nama = '{}';".format(request.session.get('email'), bibitt))
            hasil1 = tuplefetchall(c)
            for data in hasil1 :
                if int(data.jumlah) < jumlahh :
                    response = {'hasil' : hasil, 'message' : "Anda tidak memiliki bibit yang cukup, silahkan membeli bibit terlebih dahulu"}
                    return render(request, 'create_produksi_tanaman.html', response);
            c.execute("select id from aset where nama = '{}'".format(bibitt))
            hasilid = tuplefetchall(c)
            c.execute("insert into histori_produksi values ('{}', '{}', '{}', '{}', '{}')".format(request.session.get('email'), waktuu, waktuu,jumlahh,xpp))

            c.execute("insert into histori_tanaman values ('{}', '{}', '{}')".format(request.session.get('email'), waktuu, hasilid[0].id))
            
            return redirect('/histori-tanaman')