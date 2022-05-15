from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db import connection
from collections import namedtuple
from .forms import *
from django.template.defaulttags import register


# Create your views here.

def index(request):
    cursor = connection.cursor()
    result = []
    
    # email = request.POST.get('email')
    # password = request.POST.get('password')
        
    # try:
    #     cursor.execute("SET SEARCH_PATH TO hiday")
    #     cursor.execute("SELECT * FROM ADMIN WHERE ADMIN.email ='" + email + "' AND ADMIN.PASSWORD = '" + password + "'")
    #     # result = namedtuplefetchall(cursor)
        
    #     result = cursor.fetchone()
    #     cursor.close()

    #     if(result == None): 
        
    #         cursor = connection.cursor()
    #         cursor.execute("SET SEARCH_PATH TO hiday")
    #         cursor.execute("SELECT * FROM PENGGUNA WHERE PENGGUNA.email ='" + email + "' AND PENGGUNA.PASSWORD = '" + password + "'")
    #         result = cursor.fetchone()

    #         if(result == None):  
    #             pass

    #     # Redirect the cursor towards public so it can access Django basic features
    #     cursor = connection.cursor()

    #     cursor.execute("SET SEARCH_PATH TO public")
    #     request.session['email'] = [email, password, result]

    # except Exception as e:
    #     print(e)
    # finally:
    #     cursor.close()
    # print(result)

    return render(request, 'index.html', {'result': result} )

def login(request):
    if(request.method == "POST"):
        print("masuk")
        login = request.POST
        cursor = connection.cursor()
        email = login['email']
        passw = login['pass']

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
            return redirect('/admin-index')
            
        elif (len(result_pengguna) != 0):
            request.session.modified = True
            request.session['email'] = email
            request.session['role'] = 'pengguna'
            return redirect('/pengguna-index')
        else:
            print("login gagal")

    return render(request, 'login.html')

def admin_index(request):
    email = request.session.get('email')
    response = {'email': email}
    return render(request, 'admin-index.html', response)

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

    return render(request, 'pengguna-index.html', response)