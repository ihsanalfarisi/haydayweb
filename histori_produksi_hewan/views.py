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
      #   c.execute("""select * from histori_produksi;""")
        c.execute("""select hh.email,hh.waktu_awal,hp.waktu_selesai,hp.jumlah, hp.xp, 
        a.nama from histori_hewan hh, histori_produksi hp, hewan h, 
        aset a where hh.email = hp.email and hh.waktu_awal = hp.waktu_awal and 
        hh.id_hewan = h.id_aset and h.id_aset = a.id;""")
        hasil = tuplefetchall(c)
    
    response = {'hasil': hasil,}

    return render(request, 'histori_produksi_hewan.html', response)

def CreateHistoriHewan(request):
      c = connection.cursor()
      if request.method == 'POST' :
        id_hewan = request.POST.get('id_hewan')
        jumlah = request.POST.get('jumlah')
        xp = request.POST.get('xp')
        c.execute("select id_hewan from tkb08.id_hewan where id_hewan = %s",[id_hewan])
        id_hewan = tuplefetchall(c)[0]
        c.execute("INSERT INTO histori_hewan(id_hewan, jumlah, xp) VALUES (%s,%s,%s)",[id_hewan,jumlah,xp])
        return redirect('histori_produksi:CreateHistoriHewan')
      c.execute("SELECT id_hewan from tkb08.histori_hewan")
      create_histori_hewan = tuplefetchall(c)
      return render(request,'create_histori_hewan.html',{'create_histori_hewan':create_histori_hewan})