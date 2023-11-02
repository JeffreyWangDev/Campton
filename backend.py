import sqlite3 as sl
from datetime import date
import random
import string
import phonenumbers
import time

def cheekphone(phone):
    """
    Checks the validity of a phone number.

    Args:
        phone (str): The phone number to check.

    Returns:
        bool: True if the phone number is valid, False otherwise.
    """
    try:
        phnum = phonenumbers.parse("+1"+str(phone))
        if(phonenumbers.is_valid_number(phnum) == True):
            return(True)
        else:
            return(False)
    except:
        return(False)
    
def getnewid():
    """
    Generates a new unique seller ID.

    Returns:
        str: A new unique seller ID.
    """
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
    """
    Generates a new unique item ID.

    Returns:
        str: A new unique item ID.
    """
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
    """
    Creates a new seller in the database.

    Args:
        request: The request object containing seller information.

    Returns:
        int or str: 0 if the seller is successfully added, or an error message if there is an issue.
    """
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
    """
    Retrieves seller information by phone number.

    Args:
        pnum (str): The phone number of the seller.

    Returns:
        tuple: A tuple containing an error code (0 for success, 1 for error) and either seller information or an error message.
    """
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
    """
    Updates seller information in the database.

    Args:
        request: The request object containing updated seller information.

    Returns:
        int or str: 0 if the seller information is successfully updated, or an error message if there is an issue.
    """
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
    cursor.execute("UPDATE user SET sellerid =?,name=?,address=?,city=?,state=?,zip=? WHERE sellerid=?", (str(id),str(name),str(address),str(city),str(state),str(zip),str(id)))
    sqlite.commit()
    cursor.close()
    sqlite.close()
    addlog(f"UPDATESELLER: {str(id)} {str(phone)} {str(name)} {str(address)} {str(city)} {str(state)} {str(zip)} {str(id)}",request)
    return(0)
def nitem(request,name):
    """
    Adds a new item to the database.

    Args:
        request: The request object containing item information.
        name (str): The name of the item.

    Returns:
        int or str: 0 if the item is successfully added, or an error message if there is an issue.
    """
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
    """
    Retrieves item information by item ID.

    Args:
        itemid (int): The item ID to retrieve. If None, retrieves all items.

    Returns:
        tuple: A tuple containing an error code (1 for success, 2 for error) and either item information or an error message.
    """
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    item = cursor.execute("SELECT * FROM items WHERE itemid = ?", (int(itemid),)).fetchall()
    cursor.close() 
    sqlite.close()
    if item: 
        return((1,item))
    return((2,"Error: Item not found"))
def updateitem(request, name):
    """
    Updates item information in the database.

    Args:
        request: The request object containing updated item information.
        name (str): The name of the item.

    Returns:
        int or str: 0 if the item information is successfully updated, or an error message if there is an issue.
    """
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
    """
    Retrieves a report of items associated with a seller's phone number.

    Args:
        phone (str): The phone number of the seller.

    Returns:
        list: A list containing either seller information or a list of item information.
    """
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
    """
    Formats a phone number with dashes.

    Args:
        n (str): The phone number to format.

    Returns:
        str: The formatted phone number.
    """                                                                                                                              
    return format(int(n[:-1]), ",").replace(",", "-") + n[-1]   
def reporta(request):
    """
    Marks items as paid in the database and updates their status.

    Args:
        request: The request object containing seller information.

    Returns:
        int or str: 0 if the report is successful, or an error message if there is an issue.
    """
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
    """
    Marks items as sold in the database and updates their status.

    Args:
        items (dict): A dictionary of items to mark as sold.
        request: The request object.

    Returns:
        list: A list containing an error code (0 for success, 1 for item not found, 2 for item already sold) and an error message if applicable.
    """
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

    """
    Adds a log entry to the database.

    Args:
        event (str): The log event description.
        request: The request object.

    Returns:
        int: Always returns 0.
    """
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    cursor.execute("INSERT INTO log(event,ip,useragent,time) VALUES (?, ?, ?, ?)", (str(event),str(request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)),str(request.headers["User-Agent"]),str(time.time())))
    sqlite.commit()
    cursor.close()
    sqlite.close()
    return(0)
def getlog(password):
    """
    Retrieves the log entries from the database.

    Args:
        password (str): The password to access the log (must be "Password12").

    Returns:
        list: A list containing an error code (0 for wrong password, 1 for success) and the log entries if the password is correct.
    """
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
    """
    Retrieves all data from the database, including user information, item information, and log entries.

    Returns:
        list: A list containing user information, item information, and log entries.
    """
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
