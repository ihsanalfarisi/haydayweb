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
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""
        select tp.email, tp.waktu, a.nama, tp.jumlah, (tp.jumlah * a.harga_beli) total_harga
        FROM transaksi_pembelian tp
        LEFT OUTER JOIN aset a ON tp.id_aset = a.id;
        """)
        hasil = tuplefetchall(c)
        role = 'admin'
    
    response = {'hasil': hasil, 'role': role}

    return render(request, 'transaksi_pembelian_aset.html', response)