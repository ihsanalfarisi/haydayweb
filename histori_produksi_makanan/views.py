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
    if request.session.get('role') == 'pengguna':
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select hpm.email, hpm.waktu_awal, hp.waktu_selesai, hpm.id_produk_makanan, 
                        hp.jumlah, hp.xp, pk.nama as pnama, a.nama as anama
                        from histori_produksi_makanan as hpm
                        join histori_produksi as hp
                        on hpm.email = hp.email
                        join produk as pk
                        on hpm.id_produk_makanan = pk.id
                        join aset as a
                        on hpm.id_alat_produksi = a.id
                        where hpm.email = '{}';""".format(request.session.get('email')))
            hasil = tuplefetchall(c)
            role = 'pengguna'
    
    response = {'hasil': hasil, 'role' : role,}
    return render(request, 'histori_produksi_makanan.html', response)

def readadmin(request):
    if request.session.get('role') == 'admin':
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select hpm.email, hpm.waktu_awal, hp.waktu_selesai, hpm.id_produk_makanan, 
                        hp.jumlah, hp.xp, pk.nama as pnama, a.nama as anama
                        from histori_produksi_makanan as hpm
                        join histori_produksi as hp
                        on hpm.email = hp.email
                        join produk as pk
                        on hpm.id_produk_makanan = pk.id
                        join aset as a
                        on hpm.id_alat_produksi = a.id""")
            hasiladmin = tuplefetchall(c)
            role = 'admin'
        
    response = {'hasiladmin': hasiladmin, 'role' : role,}
    return render(request, 'histori_produksi_makanan_admin.html', response)

def create_makanan(request):
    if request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select hpm.email, hpm.waktu_awal, hp.waktu_selesai, hpm.id_produk_makanan, 
                        hp.jumlah, hp.xp, pk.nama as pnama, a.nama as anama
                        from histori_produksi_makanan as hpm
                        join histori_produksi as hp
                        on hpm.email = hp.email
                        join produk as pk
                        on hpm.id_produk_makanan = pk.id
                        join aset as a
                        on hpm.id_alat_produksi = a.id
                        where hpm.email = '{}';""".format(request.session.get('email')))
            hasilcreate = tuplefetchall(c)
        response = {'hasilcreate': hasilcreate}
        return render(request, 'create_produksi_makanan.html', response)


def apply_create_makanan(request):
    if request.session.get('role') == "pengguna":
        data_produksi = {
            "pnama" : request.POST.get("prod_makan"),
            "jumlah" : request.POST.get("jumlah"),
            "xp" : 5,
            "waktu" : datetime.datetime.now()
        }
        
        with connection.cursor() as c:
                c.execute("set search_path to hiday")
                c.execute("select a.nama from koleksi_aset_memiliki_aset kama, koleksi_aset ka, aset a where kama.id_koleksi_aset = ka.email and kama.id_aset = a.id and a.id like 'bt%' and ka.email = '{}';".format(request.session.get('email')))
                hasil = tuplefetchall(c)

        with connection.cursor() as c:
            if len(data_produksi['pnama'])==0:
                response = {'hasil' : hasil, 'message' : "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu"}
                return render(request, 'create_produksi_makanan.html', response);
            if len(data_produksi['jumlah'])==0:
                response = {'hasil' : hasil, 'message' : "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu"}
                return render(request, 'create_produksi_makanan.html', response);
            pr_makan= data_produksi['pnama']
            jumlahh= int(data_produksi['jumlah'])
            data_produksi['xp'] = int(data_produksi['xp']) * jumlahh
            waktuu = data_produksi['waktu']
            xpp = int(data_produksi['xp'])
            c.execute("set search_path to hiday")
            c.execute("select kama.jumlah from koleksi_aset_memiliki_aset kama, aset a where kama.id_aset = a.id and kama.id_koleksi_aset = '{}' and a.nama = '{}';".format(request.session.get('email'), pr_makan))
            hasil1 = tuplefetchall(c)
            for data in hasil1 :
                if int(data.jumlah) < jumlahh :
                    response = {'hasil' : hasil, 'message' : "Anda tidak memiliki bahan yang cukup, silahkan membeli bahan terlebih dahulu"}
                    return render(request, 'create_produksi_makanan.html', response);
            c.execute("select id from aset where nama = '{}'".format(pr_makan))
            hasilid = tuplefetchall(c)
            c.execute("insert into histori_produksi values ('{}', '{}', '{}', '{}', '{}')".format(request.session.get('email'), waktuu, waktuu,jumlahh,xpp))

            c.execute("insert into histori_produksi_makanan values ('{}', '{}', '{}', '{}')".format(request.session.get('email'), waktuu, hasilid[0].id))
            
            return redirect('histori_produksi_makanan')