import sqlite3 as sl
from datetime import date
import random
import string
import phonenumbers
import time

def cheekphone(phone):
    try:
        phnum = phonenumbers.parse("+1"+str(phone))
        if(phonenumbers.is_valid_number(phnum) == True):
            return(True)
        else:
            return(False)
    except:
        return(False)
    
def getnewid():
    link = ''.join(random.choice(string.ascii_letters+str(1234567890)) for x in range(5))
    link = link +random.choice("ABCDEFGHIJKMNORSUVWXYZ1234567890")
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    item = cursor.execute("SELECT * FROM user WHERE sellerid = ?", (str(link),)).fetchone()
    cursor.close()
    sqlite.close() 
    if item ==None: 
        return link
    else:
        return(getnewid())
def getnewiid():
    link = ''.join(random.choice(string.ascii_letters+str(1234567890)) for x in range(5))
    link = link +random.choice("ABCDEFGHIJKMNORSUVWXYZ1234567890")
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    item = cursor.execute("SELECT * FROM items WHERE itemcid = ?", (str(link),)).fetchone()
    cursor.close()
    sqlite.close() 
    if item ==None: 
        return link
    else:
        return(getnewiid())
def newseller(request):
    phonen,name,address,city,state,zip = request.form['phonen'],request.form['name'],request.form['address'],request.form['city'],request.form['state'],request.form['zip']
    if not cheekphone(phonen):
        return("Error: Phone number invalid")

    phone = str(phonen.replace(" ",""))
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    item = cursor.execute("SELECT * FROM user WHERE phone = ?", (int(phone),)).fetchone()
    cursor.close()
    sqlite.close()
    if item:
        return("Error: Phone number already in use")
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    newid = getnewid()
    cursor.execute("INSERT INTO user(sellerid,phone,name,address,city,state,zip) VALUES (?, ?, ?,?,?,?,?)", (str(newid),int(phone),str(name),str(address),str(city),str(state),str(zip)))
    sqlite.commit()
    cursor.close()
    sqlite.close()
    addlog(f"NEWSELLER: {str(newid)} {int(phone)} {str(name)} {str(address)} {str(city)} {str(state)} {str(zip)}",request)
    return(0)

def getseller(pnum):
    if not cheekphone(pnum):
        return((1,"Error: Phone number invalid"))
    phone = str(pnum.replace(" ",""))
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    item = cursor.execute("SELECT * FROM user WHERE phone = ?", (int(phone),)).fetchone()
    cursor.close() 
    sqlite.close()
    if item: 
        return((0,item))
        
    else:
        return((1,"Error: Phone number not found"))


def updateseller(request):
    phonen,name,address,city,state,zip,id = request.form['phonen'],request.form['name'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['sid']
    if not cheekphone(phonen):
        return("Error: Phone number invalid")
    phone = str(phonen.replace(" ",""))
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    item = cursor.execute("SELECT * FROM user WHERE sellerid = ?", (str(id),)).fetchone()
    cursor.close()
    sqlite.close()
    if not item:
        return("Error: User not found")
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    cursor.execute("UPDATE user SET sellerid =?,phone=?,name=?,address=?,city=?,state=?,zip=? WHERE sellerid=?", (str(id),int(phone),str(name),str(address),str(city),str(state),str(zip),str(id)))
    sqlite.commit()
    cursor.close()
    sqlite.close()
    addlog(f"UPDATESELLER: {str(id)} {str(phone)} {str(name)} {str(address)} {str(city)} {str(state)} {str(zip)} {str(id)}",request)
    return(0)
def nitem(request,name):  
    sellerphone,itemid,itemprice,itemname,itemdisc = request.form['phonen'],request.form['id'],request.form['price'],name,request.form['dis']  
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    item = cursor.execute("SELECT * FROM items WHERE itemid = ?", (str(itemid),)).fetchone()
    cursor.close()
    sqlite.close() 
    if item:
        return("Error: Item number already in use")
    a = getseller(sellerphone.replace(" ",""))
    if a[0]==1:
        return(a[1])
    a=a[1]
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    newid=getnewiid()
    cursor.execute("INSERT INTO items(sellerphone,sellerid,itemid,itemprice,itemname,itemdisc,itemstatus,itemcid) VALUES (?, ?, ?,?,?,?,?,?)", (int(a[2]),str(a[1]),str(itemid),int(itemprice),str(itemname),str(itemdisc),0,str(newid)))
    sqlite.commit()
    cursor.close()
    sqlite.close()
    addlog(f"NEWITEM: {str(a[2])} {str(a[1])} {str(itemid)} {str(itemprice)} {str(itemname)} {str(itemdisc)} {0} {str(newid)}",request)
    return(0)

def getitem(itemid=None):
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    item = cursor.execute("SELECT * FROM items WHERE itemid = ?", (int(itemid),)).fetchall()
    cursor.close() 
    sqlite.close()
    if item: 
        return((1,item))
    return((2,"Error: Item not found"))
def updateitem(request, name):
    sellerphone,itemid,itemprice,itemname,itemdisc,sold,id = request.form['phonen'],request.form['id'],request.form['price'],name,request.form['dis'],request.form['sold'],request.form['cid']
    a = getseller(sellerphone.replace(" ",""))
    if a[0]==1:
        return(a[1]) 
    a=a[1]
    b = getitem(request.form['id'])
    if b[0] == 1 and b[1][0][8] !=id:
        return("Error: Item id is already in use")
    phone = str(sellerphone.replace(" ",""))
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    item = cursor.execute("SELECT * FROM items WHERE itemcid = ?", (str(id),)).fetchone()
    cursor.close()
    sqlite.close()
    if str(sold).lower() == "not sold":
        sold=0
    elif str(sold).lower() == "sold":
        sold=1
    elif str(sold).lower() == "paid":
        sold = 2
    elif str(sold).lower() == "returned":
        sold = 3
    else:
        return('Error: Item status can only be Not sold, Sold, or Paid')
    if not item:
        return("Error: Item not found")
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    cursor.execute("UPDATE items SET sellerphone=?,sellerid=?,itemid=?,itemprice=?,itemname=?,itemdisc=?,itemstatus=? WHERE itemcid=?", (int(phone),str(a[1]),str(itemid),int(itemprice),str(itemname),str(itemdisc),sold,str(id)))
    sqlite.commit()
    cursor.close()
    sqlite.close()
    addlog(f"UPDATEITEM: {str(phone)} {str(a[1])} {str(itemid)} {str(itemprice)} {str(itemname)} {str(itemdisc)} {sold} {str(id)}",request)
    return(0)
def getreport(phone):
    phone = phone.replace(" ","")
    a = getseller(phone.replace(" ",""))
    #print(a)
    if a[0] == 1:
        return(a[1])
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    item = cursor.execute("SELECT * FROM items WHERE sellerid = ?", (str(a[1][1]),)).fetchall()
    cursor.close()
    sqlite.close()
    #print(item)
    return([0,item])

def phone_format(n):                                                                                                                                  
    return format(int(n[:-1]), ",").replace(",", "-") + n[-1]   
def reporta(request):
    phone =request.json["phone"]
    phone = phone.replace(" ","")
    a = getseller(phone.replace(" ",""))
    if a[0] == 1:
        return(a[1])
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    cursor.execute("UPDATE items SET itemstatus=2 WHERE sellerphone=? AND itemstatus = 1", (phone,))
    sqlite.commit()
    cursor.execute("UPDATE user SET paid =1 WHERE phone=?", (phone,))
    sqlite.commit()
    cursor.close()
    sqlite.close()
    addlog(f"REPORT: {str(phone)}",request)
    return(0) 
def postitems(items,request):
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    for i in items: 
        a = getitem(str(items[i]))
        if a[0]== 1:
            if a[1][0][7] == 0:
                #print("added")
                cursor.execute("UPDATE items SET itemstatus=1 WHERE itemid=?", (str(items[i]),))
                sqlite.commit()
            else:
                return([2,f"The item with an id of {items[i]} is already sold, try refreshing the page, if this is still the case then contact Jeffrey Wang"])
        else:
            return([1,f"The item with an id of {items[i]} was not found"])

    cursor.close()
    sqlite.close()
    addlog(f"CHEEKOUT: {str(items)}",request)
    return([0]) 

def addlog(event,request):
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    cursor.execute("INSERT INTO log(event,ip,useragent,time) VALUES (?, ?, ?, ?)", (str(event),str(request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)),str(request.headers["User-Agent"]),str(time.time())))
    sqlite.commit()
    cursor.close()
    sqlite.close()
    return(0)
def getlog(password):
    if password == "Password12":
        sqlite = sl.connect('main.db')
        cursor = sqlite.cursor()
        item = cursor.execute("SELECT * FROM log").fetchall()
        cursor.close()
        sqlite.close()
        return([1,item])
    else:
        return([0,"Wrong Password!"])
def getall():
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    item1 = cursor.execute("SELECT * FROM user").fetchall()
    item2 = cursor.execute("SELECT * FROM items").fetchall()
    item3 = cursor.execute("SELECT * FROM log").fetchall()
    user = []
    items = []
    log = []

    item11 = cursor.execute("SELECT * FROM user")
    a = []
    for i in item11.description:
        a.append(i[0])
    user.append(a)
    item22 = cursor.execute("SELECT * FROM items")
    b = []
    for i in item22.description:
        b.append(i[0])
    items.append(b)
    item33 = cursor.execute("SELECT * FROM log")
    c = []
    for i in item33.description:
        c.append(i[0])
    log.append(c)

    cursor.close()
    sqlite.close()
    user.extend(item1)
    items.extend(item2)
    log.extend(item3)
    return([user,items,log])
