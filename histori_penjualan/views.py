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
        c.execute("""select * from histori_penjualan;""")
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil,}

    return render(request, 'histori_penjualan.html', response)

def detail_pesanan(request):
      with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select * from detail_pesanan;""")
            hasil = tuplefetchall(c)

      response = {'hasil': hasil,}

      return render(request, 'detail_pesanan.html', response)