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
            c.execute("""select * from histori_penjualan;""")
            hasil = tuplefetchall(c)
    
        response = {'hasil': hasil,}

        return render(request, 'histori_penjualan.html', response)
    elif request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select * from histori_penjualan;""")
            hasil = tuplefetchall(c)

        response = {'hasil': hasil,}

        return render(request, 'histori_penjualan_peng.html', response)

def detailpesanan(request):
    if request.session.get('role') == "admin":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select nama, jumlah, subtotal from produk p,
            detail_pesanan dp where dp.id_pesanan = p.id;""")
            hasil = tuplefetchall(c)

        response = {'hasil': hasil,}
        return render(request, 'detail_pesanan.html', response)

    elif request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select nama, jumlah, subtotal from produk p,
            detail_pesanan dp where dp.id_pesanan = p.id;""")
            hasil = tuplefetchall(c)

        response = {'hasil': hasil,}
        return render(request, 'detail_pesanan_peng.html', response)