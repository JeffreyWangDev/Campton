"""All backend functions for the website."""
import sqlite3 as sl
import random
import string
import time
import phonenumbers

def make_database():
    """
    Makes a database and creates tables if they don't exist

    Returns:
        Nonea
    """
    acc = sl.connect('main.db')

    with acc:
        acc.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                sellerid TEXT NOT NULL,
                phone INTEGER NOT NULL,
                name TEXT,
                address TEXT, 
                city TEXT,
                state TEXT,
                zip TEXT,
                paid INTEGER
            );
        """)

    with acc:
        acc.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                sellerphone INTEGER NOT NULL,
                sellerid TEXT NOT NULL, 
                itemid TEXT NOT NULL, 
                itemprice INTEGER NOT NULL, 
                itemname TEXT NOT NULL,
                itemdisc TEXT,
                itemstatus INTEGER NOT NULL,
                itemcid TEXT NOT NULL
            );
        """)


    with acc:
        acc.execute("""
            CREATE TABLE IF NOT EXISTS log (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                event STRING,
                ip STRING,
                useragent STRING,
                time INTGER
            );
        """)

make_database()

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
        return phonenumbers.is_valid_number(phnum)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

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
    if item is None:
        return link
    return getnewid()
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
    if item is None:
        return link
    return getnewiid()
def newseller(request):
    """
    Creates a new seller in the database.

    Args:
        request: The request object containing seller information.

    Returns:
        int or str: 0 if the seller is successfully added, or an error message if there is an issue.
    """
    phonen = request.form['phonen']
    name = str(request.form['name'])
    address = str(request.form['address'])
    city = str(request.form['city'])
    state = str(request.form['state'])
    zip_code = str(request.form['zip'])
    if not cheekphone(phonen):
        return "Error: Phone number invalid"

    phone = int(phonen.replace(" ",""))
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    item = cursor.execute("SELECT * FROM user WHERE phone = ?", (phone,)).fetchone()
    cursor.close()
    sqlite.close()
    if item:
        return "Error: Phone number already in use"
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    newid = getnewid()
    cursor.execute(
        "INSERT INTO user(sellerid,phone,name,address,city,state,zip) VALUES (?, ?, ?,?,?,?,?)",
                   (newid,
                    phone,
                    name,
                    address,
                    city,
                    state,
                    zip_code))
    sqlite.commit()
    cursor.close()
    sqlite.close()
    addlog(f"NEWSELLER: {newid} {phone} {name} {address} {city} {state} {zip_code}",request)
    return 0

def getseller(pnum):
    """
    Retrieves seller information by phone number.

    Args:
        pnum (str): The phone number of the seller.

    Returns:
        tuple: A tuple containing an code (0: success, 1: error) and seller info or an error msg.
    """
    if not cheekphone(pnum):
        return (1,"Error: Phone number invalid")
    phone = str(pnum.replace(" ",""))
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    try:
        item = cursor.execute("SELECT * FROM user WHERE phone = ?", (int(phone),)).fetchone()
    except ValueError:
        return (1,"Error: Phone number invalid")
    cursor.close()
    sqlite.close()
    if item:
        return (0,item)
    return (1,"Error: Phone number not found")


def updateseller(request):
    """
    Updates seller information in the database.

    Args:
        request: The request object containing updated seller information.

    Returns:
        int or str: 0 if the seller information is updated, or an error message if issue occurs.
    """
    phonen = request.form['phonen']
    name = str(request.form['name'])
    address = str(request.form['address'])
    city = str(request.form['city'])
    state = str(request.form['state'])
    zip_code = str(request.form['zip'])
    user_id = str(request.form['sid'])
    if not cheekphone(phonen):
        return "Error: Phone number invalid"
    phone = str(phonen.replace(" ",""))
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    item = cursor.execute("SELECT * FROM user WHERE sellerid = ?", (str(user_id),)).fetchone()
    cursor.close()
    sqlite.close()
    if not item:
        return "Error: User not found"
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    cursor.execute("UPDATE user SET name=?,address=?,city=?,state=?,zip=? WHERE sellerid=?",
                   (name,
                    address,
                    city,
                    state,
                    zip_code,
                    user_id))
    sqlite.commit()
    cursor.close()
    sqlite.close()
    addlog(f"UPDATESELLER: {user_id} {phone} {name} {address} {city} {state} {zip_code}",request)
    return 0
def nitem(request,itemname:str):
    """
    Adds a new item to the database.

    Args:
        request: The request object containing item information.
        itemname (str): The name of the item.

    Returns:
        int or str: 0 if the item is successfully added, or an error message if there is an issue.
    """
    sellerphone = request.form['phonen']
    itemid = str(request.form['id'])
    itemprice = str(request.form['price'])
    itemdisc = str(request.form['dis'])
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    item = cursor.execute("SELECT * FROM items WHERE itemid = ?", (str(itemid),)).fetchone()
    cursor.close()
    sqlite.close()
    if item:
        return "Error: Item number already in use"
    a = getseller(sellerphone.replace(" ",""))
    if a[0]==1:
        return a[1]
    a=a[1]
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    newid=getnewiid()
    cursor.execute("""INSERT INTO items(
                   sellerphone,
                   sellerid,
                   itemid,
                   itemprice,
                   itemname,
                   itemdisc,
                   itemstatus,
                   itemcid) 
                   VALUES (?, ?, ?,?,?,?,?,?)""",
                   (int(a[2]),
                    str(a[1]),
                    str(itemid),
                    int(itemprice),
                    str(itemname),
                    str(itemdisc),
                    0,
                    str(newid)))
    sqlite.commit()
    cursor.close()
    sqlite.close()
    ip = itemprice
    iname = itemname
    addlog(f"NEWITEM: {str(a[2])} {str(a[1])} {itemid} {ip} {iname} {itemdisc} {0} {newid}",request)
    return 0

def getitem(itemid=None):
    """
    Retrieves item information by item ID.

    Args:
        itemid (int): The item ID to retrieve. If None, retrieves all items.

    Returns:
        tuple: A tuple with error code (1 for success, 2 for error) and item info or an error msg.
    """
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    item = cursor.execute("SELECT * FROM items WHERE itemid = ?", (int(itemid),)).fetchall()
    cursor.close()
    sqlite.close()
    if item:
        return (1,item)
    return (2,"Error: Item not found")
def updateitem(request, itemname:str):
    """
    Updates item information in the database.

    Args:
        request: The request object containing updated item information.
        name (str): The name of the item.

    Returns:
        int or str: 0 if the item information is updated, or an error msg if there is an issue.
    """

    sellerphone = str(request.form['phonen'])
    itemid = str(request.form['id'])
    ip = request.form['price']
    itemdisc = request.form['dis']
    sold = request.form['sold']
    item_id = request.form['cid']
    a = getseller(sellerphone.replace(" ",""))
    if a[0]==1:
        return a[1]
    a=a[1]
    b = getitem(item_id)
    if b[0] == 1 and b[1][0][8] != item_id:
        return "Error: Item id is already in use"
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
        return 'Error: Item status can only be Not sold, Sold, or Paid'
    if not item:
        return "Error: Item not found"
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    cursor.execute("""UPDATE items SET
                   sellerphone=?,
                   sellerid=?,
                   itemid=?,
                   itemprice=?,
                   itemname=?,
                   itemdisc=?,
                   itemstatus=? 
                   WHERE itemcid=?""", (
                       int(phone),
                       str(a[1]),
                       str(itemid),
                       int(ip),
                       str(itemname),
                       str(itemdisc),
                       sold,str(id)))
    sqlite.commit()
    cursor.close()
    sqlite.close()
    iname = itemname
    addlog(f"UPDATEITEM: {phone} {str(a[1])} {itemid} {ip} {iname} {itemdisc} {sold} {id}",request)
    return 0
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
        return a[1]
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    item = cursor.execute("SELECT * FROM items WHERE sellerid = ?", (str(a[1][1]),)).fetchall()
    cursor.close()
    sqlite.close()
    #print(item)
    return [0,item]

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
        return a[1]
    sqlite = sl.connect('main.db')
    cursor = sqlite.cursor()
    cursor.execute("UPDATE items SET itemstatus=2 WHERE sellerphone=? AND itemstatus = 1", (phone,))
    sqlite.commit()
    cursor.execute("UPDATE user SET paid =1 WHERE phone=?", (phone,))
    sqlite.commit()
    cursor.close()
    sqlite.close()
    addlog(f"REPORT: {str(phone)}",request)
    return 0

def postitems(items,request):
    """
    Marks items as sold in the database and updates their status.

    Args:
        items (dict): A dictionary of items to mark as sold.
        request: The request object.

    Returns:
        list: A list with error code (0 for success, 1 for item not found, 2 for item already sold) 
        and an error message if applicable.
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
                return [2,
                        f"""The item with an id of {items[i]} is already sold, 
                        try refreshing the page, 
                        if this is still the case then contact Jeffrey Wang"""]
        else:
            return [1,f"The item with an id of {items[i]} was not found"]

    cursor.close()
    sqlite.close()
    addlog(f"CHEEKOUT: {str(items)}",request)
    return [0]

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
    cursor.execute("INSERT INTO log(event,ip,useragent,time) VALUES (?, ?, ?, ?)",
                   (str(event),
                    str(request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)),
                    str(request.headers["User-Agent"]),
                    str(time.time())))
    sqlite.commit()
    cursor.close()
    sqlite.close()
    return 0
def getlog(password):
    """
    Retrieves the log entries from the database.

    Args:
        password (str): The password to access the log (must be "Password12").

    Returns:
        list: A list containing an error code (0 for wrong password, 1 for success) 
        and the log entries if the password is correct.
    """
    if password == "Password12":
        sqlite = sl.connect('main.db')
        cursor = sqlite.cursor()
        item = cursor.execute("SELECT * FROM log").fetchall()
        cursor.close()
        sqlite.close()
        return [1,item]
    return [0,"Wrong Password!"]
def getall():
    """
    Retrieves all data from the database: user information, item information, and log entries.

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
    return [user,items,log]
