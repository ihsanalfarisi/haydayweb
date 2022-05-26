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
            c.execute("""select * from transaksi_upgrade_lumbung;""")
            hasil = tuplefetchall(c)
        
        response = {'hasil': hasil,}

        return render(request, 'transaksi_upgrade_lumbung.html', response)
    elif request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("select * from transaksi_upgrade_lumbung where email = '{}';".format(request.session.get('email')))
            hasil = tuplefetchall(c)
        
        response = {'hasil': hasil,}

        return render(request, 'transaksi_upgrade_lumbung_peng.html', response)

def create(request):
    if request.session.get('role') == "pengguna":
        with connection.cursor() as c:
            c.execute("set search_path to hiday")
            c.execute("select * from lumbung where email = '{}';".format(request.session.get('email')))
            hasil = tuplefetchall(c)
        next_lev = int(hasil[0].level) + 1
        next_kap = int(hasil[0].kapasitas_maksimal) + 50
        next_level = str(next_lev)
        next_kapasitas = str(next_kap)
        response = {'level': hasil[0].level , 'next_level' : next_level, 'kapasitas' : hasil[0].kapasitas_maksimal, 'next_kapasitas' : next_kapasitas}
        return render(request, 'create_upgrade_lumbung.html', response)

def create_validation_upgrade_lumbung(request, level, next_level, kapasitas, next_kapasitas):
    data_lumbung = {
        "email" : request.session.get('email'),
        "next_level" : int(next_level),
        "next_kapasitas" : int(next_kapasitas),
        "message" : "",
        "level" : level,
        "kapasitas" : kapasitas
    } 

    data_upgrade = {
        "waktu" : datetime.datetime.now()
    }   

    with connection.cursor() as c:
        c.execute("set search_path to hiday")
        c.execute("select koin from pengguna where email = '{}';".format(request.session.get('email')))
        hasil = tuplefetchall(c)
        for data in hasil :
            if int(data.koin) < 200 :
                data_lumbung['message'] = "Koin anda tidak cukup, silahkan cari Koin terlebih dahulu"
                return render(request, 'create_upgrade_lumbung.html', data_lumbung);
        emaill= data_lumbung['email']
        levell= data_lumbung['next_level']
        kapasitas_maksimall= data_lumbung['next_kapasitas']
        waktuu= data_upgrade['waktu']
        c.execute("insert into transaksi_upgrade_lumbung values ('{}', '{}')".format(emaill,waktuu))
        c.execute("update lumbung set level = '{}', kapasitas_maksimal = '{}' where email = '{}';".format(levell, kapasitas_maksimall, request.session.get('email')))
    
        return redirect('/transaksi-upgrade-lumbung')