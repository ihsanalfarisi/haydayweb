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
        c.execute("""select * 
                from produk as pk
                full join detail_pesanan as dp
                on pk.id = dp.id_produk
                full join pesanan as ps
                on dp.id_pesanan = ps.id;""")
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil,}

    return render(request, 'produk.html', response)