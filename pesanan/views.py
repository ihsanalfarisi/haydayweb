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
            c.execute("""select * from pesanan;""")
            hasil = tuplefetchall(c)
    
        response = {'hasil': hasil,}

        return render(request, 'pesanan.html', response)
    elif request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select * from pesanan;""")
            hasil = tuplefetchall(c)

        response = {'hasil': hasil,}

        return render(request, 'pesanan_peng.html', response)

def detailpesanan(request):
    if request.session.get('role') == "admin" or request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("""select * from detail_pesanan;""")
            hasil = tuplefetchall(c)
    
    if request.session.get('role') == "admin":
        response = {'hasil': hasil, 'role': 'admin'}
        return render(request, 'detail_pesanan.html', response)
    else:
        response = {'hasil': hasil, 'role': 'pengguna'}
        return render(request, 'detail_pesanan.html', response)

        response = {'hasil': hasil,}

        return render(request, 'detail_pesanan.html', response)

def createpesanan(request):
    return render(request, 'create_pesanan.html', {})