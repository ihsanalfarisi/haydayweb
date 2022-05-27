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
            c.execute("""select hh.email,hh.waktu_awal,hp.waktu_selesai,hp.jumlah, hp.xp, 
            a.nama from histori_hewan hh, histori_produksi hp, hewan h, 
            aset a where hh.email = hp.email and hh.waktu_awal = hp.waktu_awal and 
            hh.id_hewan = h.id_aset and h.id_aset = a.id;""")
            hasil = tuplefetchall(c)
        
        response = {'hasil': hasil,}

        return render(request, 'histori_produksi_hewan.html', response)
    elif request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("select hh.email,hh.waktu_awal,hp.waktu_selesai,hp.jumlah, hp.xp, a.nama from histori_hewan hh, histori_produksi hp, hewan h, aset a where hh.email = hp.email and hh.waktu_awal = hp.waktu_awal and hh.id_hewan = h.id_aset and h.id_aset = a.id and hh.email = '{}';".format(request.session.get('email')))
            hasil = tuplefetchall(c)
        
        response = {'hasil': hasil,}

        return render(request, 'histori_produksi_hewan_peng.html', response)

def create_produksi(request):
    if request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("select a.nama from koleksi_aset_memiliki_aset kama, koleksi_aset ka, aset a where kama.id_koleksi_aset = ka.email and kama.id_aset = a.id and a.id like 'h%' and ka.email = '{}';".format(request.session.get('email')))
            hasil = tuplefetchall(c)
        response = {'hasil': hasil}
        return render(request, 'create_histori_hewan.html', response)

def create_validation_produksi_hewan(request):
    if request.session.get('role') == "pengguna":
        data_produksi = {
            "hewan" : request.POST.get("namaHewan"),
            "jumlah" : request.POST.get("jumlah"),
            "xp" : 5,
            "waktu" : datetime.datetime.now()
        }
        
        with connection.cursor() as c:
                c.execute("set search_path to hiday")
                c.execute("select a.nama from koleksi_aset_memiliki_aset kama, koleksi_aset ka, aset a where kama.id_koleksi_aset = ka.email and kama.id_aset = a.id and a.id like 'h%' and ka.email = '{}';".format(request.session.get('email')))
                hasil = tuplefetchall(c)

        with connection.cursor() as c:
            if len(data_produksi['hewan'])==0:
                response = {'hasil' : hasil, 'message' : "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu"}
                return render(request, 'create_histori_hewan.html', response);
            if len(data_produksi['jumlah'])==0:
                response = {'hasil' : hasil, 'message' : "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu"}
                return render(request, 'create_histori_hewan.html', response);
            hewann= data_produksi['hewan']
            jumlahh= int(data_produksi['jumlah'])
            data_produksi['xp'] = int(data_produksi['xp']) * jumlahh
            waktuu = data_produksi['waktu']
            xpp = int(data_produksi['xp'])
            c.execute("set search_path to hiday")
            c.execute("select kama.jumlah from koleksi_aset_memiliki_aset kama, aset a where kama.id_aset = a.id and kama.id_koleksi_aset = '{}' and a.nama = '{}';".format(request.session.get('email'), hewann))
            hasil1 = tuplefetchall(c)
            for data in hasil1 :
                if int(data.jumlah) < jumlahh :
                    response = {'hasil' : hasil, 'message' : "Anda tidak memiliki bibit yang cukup, silahkan membeli bibit terlebih dahulu"}
                    return render(request, 'create_histori_hewan.html', response);
            c.execute("select id from aset where nama = '{}'".format(hewann))
            hasilid = tuplefetchall(c)
            c.execute("insert into histori_produksi values ('{}', '{}', '{}', '{}', '{}')".format(request.session.get('email'), waktuu, waktuu,jumlahh,xpp))

            c.execute("insert into histori_hewan values ('{}', '{}', '{}')".format(request.session.get('email'), waktuu, hasilid[0].id))
            
            return redirect('/histori-produksi-hewan')