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
        c.execute("""select lmp.id_lumbung, lmp.id_produk, p.nama, p.harga_jual, p.sifat_produk, lmp.jumlah 
        from lumbung_memiliki_produk lmp, produk p, produk_makanan pm 
        where pm.id_produk = p.id and lmp.id_produk = p.id;""")
        hasilmakanan = tuplefetchall(c)

        c.execute("""select lmp.id_lumbung, lmp.id_produk, p.nama, p.harga_jual, p.sifat_produk, lmp.jumlah 
        from lumbung_memiliki_produk lmp, produk p, hasil_panen hp 
        where hp.id_produk = p.id and lmp.id_produk = p.id;""")
        hasilpanen = tuplefetchall(c)

        c.execute("""select lmp.id_lumbung, lmp.id_produk, p.nama, p.harga_jual, p.sifat_produk, lmp.jumlah 
        from lumbung_memiliki_produk lmp, produk p, produk_hewan ph 
        where ph.id_produk = p.id and lmp.id_produk = p.id;""")
        hasilhewan = tuplefetchall(c)
    
    response = {'hasilmakanan': hasilmakanan,'hasilpanen': hasilpanen,'hasilhewan': hasilhewan,}

    return render(request, 'lumbung.html', response)

def readadmin(request):
    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("""select lmp.id_lumbung, lmp.id_produk, p.nama, p.harga_jual, p.sifat_produk, lmp.jumlah 
        from lumbung_memiliki_produk lmp, produk p, produk_makanan pm 
        where pm.id_produk = p.id and lmp.id_produk = p.id;""")
        hasilmakanan = tuplefetchall(c)

        c.execute("""select lmp.id_lumbung, lmp.id_produk, p.nama, p.harga_jual, p.sifat_produk, lmp.jumlah 
        from lumbung_memiliki_produk lmp, produk p, hasil_panen hp 
        where hp.id_produk = p.id and lmp.id_produk = p.id;""")
        hasilpanen = tuplefetchall(c)

        c.execute("""select lmp.id_lumbung, lmp.id_produk, p.nama, p.harga_jual, p.sifat_produk, lmp.jumlah 
        from lumbung_memiliki_produk lmp, produk p, produk_hewan ph 
        where ph.id_produk = p.id and lmp.id_produk = p.id;""")
        hasilhewan = tuplefetchall(c)
    
    response = {'hasilmakanan': hasilmakanan,'hasilpanen': hasilpanen,'hasilhewan': hasilhewan,}

    return render(request, 'lumbung_admin.html', response)
