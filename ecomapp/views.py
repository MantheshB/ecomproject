
from django.shortcuts import render,HttpResponse,redirect
from django.db import connection
from django.http import HttpResponse
from django.views.generic import View
import pymysql

# Create your views here.

cr=[]
amount_payable=0



def Register(request):
    #if request.method='POST':
        #return render(request,'more_info')



    cur = connection.cursor()
    cur.execute(" select pid,pname,image,price,(price-(price*discount/100)) 'offer_price',pdesc,(CASE WHEN stock <> '0' THEN 'In Stock' ELSE 'No Stock' END) AS availability from onlineshopy.products")
    products = cur.fetchall()
    mylist = []
    for row in products:
        mylist.append(row)
        print(row)
    print(mylist)
    return render(request, 'index.html', {'mylist': mylist})



def more_info(request,pid):
    cur=connection.cursor()
    args=(pid)
    sql="select pid,pname,image,price,(price-(price*discount/100)) 'offer_price',pdesc,(CASE WHEN stock <> '0' THEN 'In Stock' ELSE 'No Stock' END) AS availability from onlineshopy.products where pid=(%s)"
    args=(pid)
    cur.execute(sql,args)
    products_info = cur.fetchall()
    mylist=[]
    for row in products_info:
        mylist.append(row)
    print(mylist)
    return render(request, 'more_info.html', {'mylist': mylist})


def cart(request,pid):
    cur = connection.cursor()
    sql = "select pid,pname,image,price,(price-(price*discount/100)) 'offer_price',pdesc,(CASE WHEN stock <> '0' THEN 'In Stock' ELSE 'No Stock' END) AS availability from onlineshopy.products where pid=(%s)"
    updatesql= "update onlineshopy.products  set stock=stock-1 where pid=(%s)"
    args=(pid)
    cur.execute(updatesql,args)
    cur.execute("commit")
    cur.execute(sql,args)
    products_info = cur.fetchall()
    for row in products_info:
        cr.append(row)
        print(row[4])
        global amount_payable
        amount_payable=amount_payable+row[4]
    print(amount_payable)
    print(cr)
    return render(request, 'cart.html', {'cr': cr,'amount_payable':amount_payable})



def checkout(request,amount_payable):



   #cur = connection.cursor()
    #cur.execute("SELECT * FROM onlineshopy.orders")
    #orders=cur.fetchall()
    #mylist=[]

    return render(request,'checkout.html',{'amount_payable':amount_payable})




def final_checkout(request):
    if request.method=='POST':
        cur=connection.cursor()
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        address = request.POST.get('address','')
        mobile = request.POST.get('mobile', '')
        city = request.POST.get('city', '')
        pin = request.POST.get('pincode', '')
        #print(pin   )
        sql = "INSERT INTO onlineshopy.orders (Name,Email,Address,Mobile,city,pincode) VALUES (%s,%s,%s,%s,%s,%s)"
        args = (name,email,address,mobile,city,pin)
        print(sql)
        print(args)
        cur.execute(sql, args)
        cur.execute('commit')
        return HttpResponse("<h1>Your Goods will be Delivered within 3 Working Days</h1>")

