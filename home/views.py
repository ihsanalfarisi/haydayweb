from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db import connection
from collections import namedtuple
from django.contrib import messages

from .forms import *
from django.template.defaulttags import register

# Create your views here.

def index(request):
    cursor = connection.cursor()
    if request.session.get('role') == "admin":
        role = request.session.get('role')
        email = request.session.get('email')
        response = {'email': email, 'role': role}
        return render(request, 'index.html', response)
    elif request.session.get('role') == "pengguna":
        role = request.session.get('role')
        email = request.session.get('email')
        print(email)
        cursor = connection.cursor()
        query = f"select email, nama_area_pertanian, xp, koin, level from hiday.pengguna where email='{email}'"
        cursor.execute(query)
        pengguna = cursor.fetchall()
        print(pengguna)
        
        response = {
            'Email': pengguna[0][0],
            'Nama_Area_Pertanian': pengguna[0][1],
            'XP': pengguna[0][2],
            'Koin': pengguna[0][3],
            'Level': pengguna[0][4],
            'role' : role
        }
        return render(request, 'index.html', response)
    role = ""
    return render(request, 'index.html', {'role': role} )

def login(request):
    if(request.method == "POST"):
        print("masuk")
        login = request.POST
        cursor = connection.cursor()
        email = login['email']
        passw = login['pass']

        if (email == '' or passw == ''):
            messages.error(request,"Data belum lengkap, silakan lengkapi data terlebih dahulu.")

        else:    
            admin = f"select email from hiday.admin where email='{email}' and password='{passw}'"
            cursor.execute(admin)
            result_admin = cursor.fetchall()
            
            pengguna = f"select email from hiday.pengguna where email='{email}' and password='{passw}'"
            cursor.execute(pengguna)
            result_pengguna = cursor.fetchall()
            
            if (len(result_admin) != 0):
                print(email)
                request.session.modified = True
                request.session['email'] = email
                request.session['role'] = 'admin'
                return redirect('home')
                
            elif (len(result_pengguna) != 0):
                request.session.modified = True
                request.session['email'] = email
                request.session['role'] = 'pengguna'
                return redirect('home')
            else:
                messages.error(request,"Email/Password invalid.")
                print("login gagal")

    return render(request, 'login.html')

def admin_index(request):
    email = request.session.get('email')
    response = {'email': email}
    return render(request, 'index.html', response)

def pengguna_index(request):
    email = request.session.get('email')
    print(email)
    cursor = connection.cursor()
    query = f"select email, nama_area_pertanian, xp, koin, level from hiday.pengguna where email='{email}'"
    cursor.execute(query)
    pengguna = cursor.fetchall()
    print(pengguna)
    
    response = {
        'Email': pengguna[0][0],
        'Nama_Area_Pertanian': pengguna[0][1],
        'XP': pengguna[0][2],
        'Koin': pengguna[0][3],
        'Level': pengguna[0][4]
    }

    return render(request, 'index.html', response)

def register(request):
    return render(request, 'register.html')

def register_admin(request):
    if(request.method == "POST"):
        print("masuk")
        register = request.POST
        cursor = connection.cursor()
        email = register['email']
        passw = register['pass']
        
        if (email == '' or passw == ''):
            messages.error(request,"Data belum lengkap, silakan lengkapi data terlebih dahulu.")

        else:
            valid = f"select email from hiday.akun where email = '{email}'"
            cursor.execute(valid)
            cek = cursor.fetchall()
            if cek == []:
                akun = f"insert into hiday.akun values ('{email}')"
                cursor.execute(akun)

                pengguna = f"insert into hiday.admin values ('{email}', '{passw}')"
                cursor.execute(pengguna)
                cursor.close()

                request.session.modified = True
                request.session['email'] = email
                request.session['role'] = 'admin'
            
                return redirect('home')
            else:
                messages.error(request,"Email sudah terdaftar.")

    return render(request, 'register-admin.html')

def register_peng(request):
    if(request.method == "POST"):
        print("masuk")
        register = request.POST
        cursor = connection.cursor()
        email = register['email']
        passw = register['pass']
        nama_area = register['nama_area']
        
        if (email == '' or passw == ''):
            messages.error(request,"Data belum lengkap, silakan lengkapi data terlebih dahulu.")

        else:
            valid = f"select email from hiday.akun where email = '{email}'"
            cursor.execute(valid)
            cek = cursor.fetchall()
            if cek == []:
                akun = f"insert into hiday.akun values ('{email}')"
                cursor.execute(akun)

                pengguna = f"insert into hiday.pengguna values ('{email}', '{passw}', '{nama_area}')"
                cursor.execute(pengguna)
                cursor.close()

                request.session.modified = True
                request.session['email'] = email
                request.session['role'] = 'pengguna'
            
                return redirect('home')
            else:
                messages.error(request,"Email sudah terdaftar.")


    return render(request, 'register-peng.html')

def logout(request):
    request.session.clear()
    # return render(request, 'index.html')
    return redirect('home')
