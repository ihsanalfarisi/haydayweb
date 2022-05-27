from django.shortcuts import render, redirect

# Create your views here.
from django.db import connection
from collections import namedtuple

import produk

def tuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def read(request):
    if request.session.get('role') == 'pengguna':
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select * from produk;""")
            #c.execute("""select pk.id as idprod, pk.nama as namaprod, pk.harga_jual, pk.sifat_produk, dp.id_pesanan, dp.no_urut, 
               # dp.subtotal, dp.jumlah, dp.id_produk, ps.id as idpes, ps.status, ps.jenis, ps.nama as namapes, ps.total
               # from produk as pk
               # join detail_pesanan as dp
               # on pk.id = dp.id_produk
               # join pesanan as ps
               # on dp.id_pesanan = ps.id;""")
            hasil = tuplefetchall(c)
            
    response = {'hasil': hasil}
    return render(request, 'produk.html', response)

def readadmin(request):
    if request.session.get('role') == 'admin':
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select * from produk;""")
            #c.execute("""select pk.id as idprod, pk.nama as namaprod, pk.harga_jual, pk.sifat_produk, dp.id_pesanan, dp.no_urut, 
               # dp.subtotal, dp.jumlah, dp.id_produk, ps.id as idpes, ps.status, ps.jenis, ps.nama as namapes, ps.total
               # from produk as pk
               # join detail_pesanan as dp
               # on pk.id = dp.id_produk
               # join pesanan as ps
               # on dp.id_pesanan = ps.id;""")
            hasiladmin = tuplefetchall(c)
            
    response = {'hasiladmin': hasiladmin,}
    return render(request, 'produk_admin.html', response)

def create_produk(request):
    if request.session.get('role') == "admin":
        ##hasilcreate = ('Hasil Panen', 'Produk Hewan', 'Produk Makanan')
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select distinct ps.jenis
        from produk as pk
        left outer join detail_pesanan as dp
        on pk.id = dp.id_produk
        left outer join pesanan as ps
        on dp.id_pesanan = ps.id;""")
            hasilcreate = tuplefetchall(c)
        
        response = {'hasilcreate': hasilcreate,}
        return render(request, 'create_produk.html', response)

def apply_create_produk(request):
    if request.session.get('role') == "admin":
        data_produk = {
            "produk" : request.POST.get("produk"),
            "harga_jual" : request.POST.get("harga_jual"),
            "nama" : request.POST.get("nama"),
            "sifat_produk" : request.POST.get("sifat_produk")
        }

        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select pk.id as idprod, pk.nama as namaprod, pk.harga_jual, pk.sifat_produk, dp.id_pesanan, dp.no_urut, 
                dp.subtotal, dp.jumlah, dp.id_produk, ps.id as idpes, ps.status, ps.jenis, ps.nama as namapes, ps.total
                from produk as pk
                join detail_pesanan as dp
                on pk.id = dp.id_produk
                join pesanan as ps
                on dp.id_pesanan = ps.id;""")
            hasilcreate = tuplefetchall(c)
            if len(data_produk['produk'])==0:
                response = {'hasilcreate': hasilcreate, 'message': "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu"}
                return render(request, 'create_produk.html', response);
            if len(data_produk['harga_jual'])==0:
                response = {'hasilcreate': hasilcreate, 'message': "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu"}
                return render(request, 'create_produk.html', response);
            if len(data_produk['nama'])==0:
                response = {'hasilcreate': hasilcreate, 'message': "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu"}
                return render(request, 'create_produk.html', response);
            if len(data_produk['sifat_produk'])==0:
                response = {'hasilcreate': hasilcreate, 'message': "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu"}
                return render(request, 'create_produk.html', response);
            
            
            produkk = data_produk['produk']
            harga_ju = int(data_produk['harga_jual'])
            nam = data_produk['nama']
            sifat_prod = data_produk['sifat_produk']
            if produkk == "Hasil Panen" :
                c.execute("set search_path to hiday")
                c.execute("""select * from hasil_panen """)
                print("Makan1")
                hasil = tuplefetchall(c)
                count = 0
                for x in hasil:
                    count+=1
                print(count)
                if count< 9:
                    idauto = "HP0{}".format(count+1)
                else:
                    idauto = "HP{}".format(count+1)
                c.execute("insert into produk values ('{}', '{}', '{}', '{}')".format(idauto, nam, harga_ju, sifat_prod))
                c.execute("insert into hasil_panen values ('{}')".format(idauto))
                print("masuk1")
                return redirect('produk_admin')

            elif produkk == "Produk Hewan" :
                c.execute("set search_path to hiday")
                c.execute("""select * from produk_hewan """)
                print("Makan2")
                hasil = tuplefetchall(c)
                count = 0
                for x in hasil:
                    count+=1
                print(count)
                if count< 9:
                    idauto = "PH0{}".format(count+1)
                else:
                    idauto = "PH{}".format(count+1)
                c.execute("insert into produk values ('{}', '{}', '{}', '{}')".format(idauto, nam, harga_ju, sifat_prod))
                c.execute("insert into produk_hewan values ('{}')".format(idauto))
                print("masuk2")
                return redirect('produk_admin')

            else : 
                c.execute("set search_path to hiday")
                c.execute("""select * from produk_makanan """)
                print("Makan3")
                hasil = tuplefetchall(c)
                count = 0
                for x in hasil:
                    count+=1
                print(count)
                if count< 9:
                    idauto = "PM0{}".format(count+1)
                else:
                    idauto = "PM{}".format(count+1)
                c.execute("insert into produk values ('{}', '{}', '{}', '{}')".format(idauto, nam, harga_ju, sifat_prod))
                c.execute("insert into produk_makanan values ('{}')".format(idauto))
                print("masuk3")
                return redirect('produk_admin')

def check_produk(request, produk):
    response = {'id' : produk,} 

    return render(request, 'update_produk.html', response)


def update_produk(request, produk):
    print(produk)
    data_produk = {
            "id" : produk,
            "harga_jual" : request.POST.get("harga_jual"),
            "nama" : request.POST.get("nama"),
            "sifat_produk" : request.POST.get("sifat_produk"),
            "message" : " "

        }

    if len(data_produk['harga_jual'])==0:
        data_produk['message'] =  "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu"
        return render(request, 'update_produk.html', data_produk);
    elif len(data_produk['sifat_produk'])==0:
        data_produk['message'] =  "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu"
        return render(request, 'update_produk.html', data_produk);

    data_produk['harga_jual'] = int(data_produk['harga_jual'])
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        produkk = data_produk['id']
        hargaa = data_produk['harga_jual']
        sifatt = data_produk['sifat_produk']
        print(produkk)
        print(hargaa)
        print(sifatt)
        c.execute("update produk set harga_jual = '{}', sifat_produk =  '{}' where id = '{}'".format(hargaa, sifatt, produkk))
        return redirect('/produk/produk-admin')


def delete_produk(request, produk):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("delete from produk where id = '{}'".format(produk))
    
    return redirect('/produk/produk-admin')