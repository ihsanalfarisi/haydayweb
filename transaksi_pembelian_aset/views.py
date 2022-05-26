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
            c.execute("""
            select tp.email, tp.waktu, substring(a.id,0,2) id, a.nama, tp.jumlah, (tp.jumlah * a.harga_beli) total_harga
            FROM transaksi_pembelian tp
            LEFT OUTER JOIN aset a ON tp.id_aset = a.id;
            """)
            hasil = tuplefetchall(c)
            role = 'admin'
    
    elif request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""
            select tp.waktu, substring(a.id,0,2) id, a.nama, tp.jumlah, (tp.jumlah * a.harga_beli) total_harga
            FROM transaksi_pembelian tp
            LEFT OUTER JOIN aset a ON tp.id_aset = a.id
            WHERE
            tp.email = '{}';""".format(request.session.get('email')))
            hasil = tuplefetchall(c)
            role = 'pengguna'
    
    response = {'hasil': hasil, 'role': role}

    return render(request, 'transaksi_pembelian_aset.html', response)

def create(request):
    role= "pengguna"
    if(request.method == "POST"):
        print("masuk")
        beli = request.POST
        cursor = connection.cursor()
        jumlah = beli['jumlah']
        id = beli['id']
        email = request.session.get('email')
        print(id)

        beli_aset = f"insert into hiday.transaksi_pembelian values ('{email}', '{datetime.datetime.now()}', {jumlah}, '{id}')"
        cursor.execute(beli_aset)
        cursor.close()
    
        return redirect('transaksi_pembelian_aset')

    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""
        select substring(a.id, 0, 2) id, a.nama, a.harga_beli, a.id as idf
        from ASET a
        ;""")
        hasil = tuplefetchall(c)

    response = {'hasil': hasil, 'role': role}

    return render(request, 'buat_pembelian.html', response)