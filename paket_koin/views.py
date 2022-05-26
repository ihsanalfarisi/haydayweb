from urllib import response
from django.shortcuts import render,redirect

# Create your views here.
from django.db import connection
from collections import namedtuple

import paket_koin, datetime

def tuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def read_paketkoin(request):
    if request.session.get('role') == "admin":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select * from paket_koin;""")
            hasil = tuplefetchall(c)
        
        response = {'hasil': hasil,}

        return render(request, 'paket_koin.html', response)
    elif request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select * from paket_koin;""")
            hasil = tuplefetchall(c)
        
        response = {'hasil': hasil,}

        return render(request, 'paket_koin_peng.html', response)

def read_transaksi(request):
    if request.session.get('role') == "admin":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select * from transaksi_pembelian_koin;""")
            hasil = tuplefetchall(c)
        
        response = {'hasil': hasil,}

        return render(request, 'transaksi_pembelian_koin.html', response)
    elif request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("select * from transaksi_pembelian_koin where email = '{}';".format(request.session.get('email')))
            hasil = tuplefetchall(c)
        
        response = {'hasil': hasil,}

        return render(request, 'transaksi_pembelian_koin_peng.html', response)

def create_paketkoin(request):
    if request.session.get('role') == "admin":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select * from paket_koin;""")
            hasil = tuplefetchall(c)
        
        response = {'hasil': hasil,}
        return render(request, 'create_paket_koin.html', {})

def create_validation_paketkoin(request):
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

def check_jumlah_transaksi(request,paket_koin, harga):
    response = {'paket_koin' : paket_koin, 'harga' : harga} 

    return render(request, 'create_transaksi_pembelian_koin.html', response)

def create_validation_transaksi(request, paket_koin):
    data_transaksi = {
        "email" : request.session.get('email'),
        "waktu" : datetime.datetime.now(),
        "jumlah" : request.POST.get("jumlah"),
        "cara_pembayaran" : request.POST.get("cara_pembayaran"),
        "paket_koin" : paket_koin,
        "total_biaya" : 0,
        'message' : '',
        'harga' : 0
    }       
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("select harga from paket_koin where jumlah_koin = '{}'".format(paket_koin))
        hasil = tuplefetchall(c)

      

    if len(data_transaksi['jumlah'])==0:
        data_transaksi['message'] =  "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu"

        return render(request, 'create_transaksi_pembelian_koin.html', data_transaksi);
    if len(data_transaksi['cara_pembayaran'])==0:
        data_transaksi['message'] =  "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu"

        return render(request, 'create_transaksi_pembelian_koin.html', data_transaksi);

    data_transaksi['jumlah'] = int(data_transaksi['jumlah'])
    data_transaksi['harga'] = hasil[0].harga
    data_transaksi['total_biaya'] = int(data_transaksi['harga']) * data_transaksi['jumlah']  

    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        emaill= data_transaksi['email']
        waktuu= data_transaksi['waktu']
        jumlahh= data_transaksi['jumlah']
        cara_pembayarann= data_transaksi['cara_pembayaran']
        paket_koinn= data_transaksi['paket_koin']
        total_biayaa= data_transaksi['total_biaya']
        c.execute("insert into transaksi_pembelian_koin values ('{}', '{}', '{}', '{}', '{}', '{}')".format(emaill,waktuu,jumlahh,cara_pembayarann,paket_koinn,total_biayaa))
    
        return redirect('/paket-koin/transaksi/read')

def check_koin(request,paket_koin):
    response = {'paket_koin' : paket_koin,} 

    return render(request, 'update_paket_koin.html', response)

def update_koin(request, paket_koin):
    data_transaksi = {
        "paket_koin" : paket_koin,
        'harga' : request.POST.get("harga"),
        'message' : ''
    }

    if len(data_transaksi['harga'])==0:
        data_transaksi['message'] =  "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu"
        return render(request, 'update_paket_koin.html', data_transaksi);

    data_transaksi['harga'] = int(data_transaksi['harga'])
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        paket_koinn= data_transaksi['paket_koin']
        hargaa = data_transaksi['harga']
        c.execute("update paket_koin set harga = '{}' where jumlah_koin = '{}'".format(hargaa, paket_koinn))
        return redirect('/paket-koin/paket_koin/read')

def delete_koin(request, paket_koin):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("delete from paket_koin where jumlah_koin = '{}'".format(paket_koin))
    
    return redirect('/paket-koin/paket_koin/read')