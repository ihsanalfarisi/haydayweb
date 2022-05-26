from django.db import connection
# from . import 

def dictfetchall(cursor):
      columns = [col[0] for col in cursor.description]
      return[dict(zip(columns, row)) for row in cursor.fetchall()]

def getDP():
      c = connection.cursor()
      text = "select nama from hiday.produk;"
      c.execute(text)
      temp = dictfetchall(c)

      return temp

def getIdPesanan():
      listId = []
      listDP = getDP()

      for i in range (len(listDP)):
            it = listDP[i]['nama']
            c = connection.cursor()

            text = "select max(id) from hiday.pesanan where detailpesanan = "
            text += "'" + it + "';"

            c.execute(text)
            temp = dictfetchall(c)

            if temp[0]['max'] != None:
                  temp[0]['max'] = str(int(temp[0]['max']) + 1)
                  temp[0]['nama'] = it

            else:
                  temp[0]['nama'] = it
                  temp[0]['max'] = '00001'

            listId.append(temp[0])

      return listId

def addPesanan(target):
      c = connection.cursor()
      id = target['detailPesanan'].split()[0]
      nama = target['namaPesanan']
      jenis = target['jenisPesanan']
      # detailPesanan = target['detailPesanan'].split()[1]

      text = "insert into hiday.pesanan values ("
      text += "'" + id + "', Baru Dipesan, " + jenis + "', '" + nama + "', 0);"

      # c.execute(text)

      return id


      