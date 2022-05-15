from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.db import connection
from collections import namedtuple
from .forms import *
from django.template.defaulttags import register


# Create your views here.

def index(request):
    cursor = connection.cursor()
    result = []
    
    email = request.POST.get('email')
    password = request.POST.get('password')
        
    try:
        cursor.execute("SET SEARCH_PATH TO hiday")
        cursor.execute("SELECT * FROM ADMIN WHERE ADMIN.email ='" + email + "' AND ADMIN.PASSWORD = '" + password + "'")
        # result = namedtuplefetchall(cursor)
        
        result = cursor.fetchone()
        cursor.close()

        if(result == None): 
        
            cursor = connection.cursor()
            cursor.execute("SET SEARCH_PATH TO hiday")
            cursor.execute("SELECT * FROM PENGGUNA WHERE PENGGUNA.email ='" + email + "' AND PENGGUNA.PASSWORD = '" + password + "'")
            result = cursor.fetchone()

            if(result == None):  
                pass

        # Redirect the cursor towards public so it can access Django basic features
        cursor = connection.cursor()

        cursor.execute("SET SEARCH_PATH TO public")
        request.session['email'] = [email, password, result]

    except Exception as e:
        print(e)
    finally:
        cursor.close()
    print(result)

    return render(request, 'index.html', {'result': result} )

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def login(request):
    cursor = connection.cursor()
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            cursor.execute("SET SEARCH_PATH TO hiday")
            cursor.execute("SELECT * FROM ADMIN WHERE ADMIN.email ='" + email + "' AND ADMIN.PASSWORD = '" + password + "'")
            # result = namedtuplefetchall(cursor)
            
            result = cursor.fetchone()
            cursor.close()

            if(result == None): 
                
                cursor = connection.cursor()
                cursor.execute("SET SEARCH_PATH TO hiday")
                cursor.execute("SELECT * FROM PENGGUNA WHERE PENGGUNA.email ='" + email + "' AND PENGGUNA.PASSWORD = '" + password + "'")
                result = cursor.fetchone()

                if(result == None):  
                    return HttpResponseNotFound("The user does not exist")
                else:
                    print(result[0])
                    res = {'email': result[0], 'pass': result[1]}
                    print(res['email'])
                    return render(request, 'index.html', res)

            # Redirect the cursor towards public so it can access Django basic features
            cursor = connection.cursor()
            cursor.execute("SET SEARCH_PATH TO public")
            request.session['email'] = [email, password, result]
            return render(request, 'index.html')

        except Exception as e:
            print(e)
        finally:
            cursor.close()
    return render(request, 'login.html', {'result': ''})
