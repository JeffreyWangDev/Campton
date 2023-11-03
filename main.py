""""Database for the app"""
import sqlite3 as sl
import werkzeug
from flask import Flask,redirect,render_template,request,url_for,jsonify, send_file
#from backend import *
import backend
app = Flask(__name__)

@app.route('/goto', methods=['GET', 'POST'])
def goto():

    place = request.args.get('place', None)
    try:
        return redirect(url_for(place))
    except werkzeug.routing.exceptions.BuildError:
        return redirect(url_for("home"))

@app.route('/')
def home():

    msg = request.args.get('msg', None)
    return render_template("home.html",msg=msg)
@app.route('/make')
def make():

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

    return "Done"
@app.route('/register', methods=['GET', 'POST'])
def register():

    error = request.args.get('error', None)
    msg = request.args.get('msg', None)
    if request.method == 'POST':
        a = backend.newseller(request)
        if a !=0:
            error = a
        else:
            return redirect(url_for('home', msg="User added"))
    return render_template('register.html', error=error,msg=msg)

@app.route('/r2', methods=['GET', 'POST'])
def register2():

    error = None
    if request.method == 'POST':
        a = backend.newseller(request)
        if a !=0:
            error = a
        else:
            return redirect(url_for('register', msg="User added"))
    return redirect(url_for('register', error=error))

@app.route('/seller', methods=['GET', 'POST'])
def seller():

    error = None
    if request.method == 'POST':
        a = list(backend.getseller(request.form['phonenn']))
        if a[0]==0:
            aa = list(a[1])
            aa[2] = backend.phone_format(str(aa[2])).replace("-"," ")
            return render_template('user.html', user=aa)
        else:
            error = a[1]
    return render_template("user.html", error=error)

@app.route('/update', methods=['GET', 'POST'])
def update():

    error = request.args.get('error', None)
    user = request.args.get('user', None)
    if request.method == 'POST':
        a = backend.updateseller(request)
        if a !=0:
            error = a
            phone = request.form['phonen']
            name = request.form['name']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            zip_code = request.form['zip']
            user = (1,1,phone,name,address,city,state,zip_code)
        else:
            return redirect(url_for('home', msg="User updated"))
    return render_template("user.html", uerror=error , user = user)

@app.route('/u2', methods=['GET', 'POST'])
def update2():

    return redirect(url_for('seller'))

@app.route('/newitem', methods=['GET', 'POST'])
def newitem():

    error = request.args.get('error', None)
    phone = request.args.get('phone', None)
    msg = request.args.get('msg', None)
    if request.method == 'POST':
        if str(request.form['name']) == "1":
            name = request.form['tname']
            if not name:
                name = "Other"
                print("here")
        else:
            name = request.form['name']
        a = backend.nitem(request,name)
        if a !=0:
            error = a
        else:
            return redirect(url_for('home', msg="Item added"))
    if phone:
        return render_template("newitem.html",error = error,phone = phone,msg=msg)
    return render_template("newitem.html",error = error,msg=msg)

@app.route('/i2', methods=['GET', 'POST'])
def newitem2():

    error = None
    if request.method == 'POST':
        if str(request.form['name']) == "1":
            name = request.form['tname']
            if not name:
                name = "Other"
        else:
            name = request.form['name']
        a = backend.nitem(request,name)
        if a !=0:
            error = a
            return redirect(url_for('newitem', error=error,phone=request.form['phonen']))
        else:
            return redirect(url_for('newitem', msg="Item added",phone=request.form['phonen']))
            #return redirect(url_for('newitem', msg="Item added"))
    return redirect(url_for('newitem', error=error))

@app.route('/item', methods=['GET', 'POST'])
def item():

    error = request.args.get('error', None)
    item_data = request.args.get('item', None)
    try:
        item_data = item_data.split("_____")
        if item_data[0] == "0":
            pass
        else:
            raise ValueError
    except (ValueError, IndexError):
        item_data = None
    if item_data:
        return render_template('item.html',item = item_data,ierror=error)
    if request.method == 'POST':
        a = list(backend.getitem(request.form['tid']))
        if a[0]==1:
            item_data = list(a[1][0])
            item_data[1] = backend.phone_format(str(item_data[1])).replace("-"," ")
            if item_data[7] ==0:
                item_data[7]="Not Sold"
            elif item_data[7]==1:
                item_data[7] = "Sold"
            elif item_data[7] == 2:
                item_data[7] = "Paid"
            elif item_data[7] == 3:
                item_data[7] = "Returned"
            return render_template('item.html',item = item)
        else:
            error = a[1]
    return render_template("item.html", error=error)

@app.route('/itemu', methods=[ 'POST'])
def itemu():

    if request.method == 'POST':
        if str(request.form['name']) == "1":
            name = request.form['tname']
            if not name:
                name = "Other"
        else:
            name = request.form['name']
        a = backend.updateitem(request,name)
        if a==0:
            return redirect(url_for("home",msg = "Item updated"))
        else:
            item_data ="".join(str(e)+"_____" for e in[
                0,
                request.form['phonen'],
                0,
                request.form['id'],
                request.form['price'],
                request.form['name'],
                request.form['dis'],
                request.form['sold'],
                request.form['cid']])
            return redirect(url_for("item",error = a,item=item_data))

@app.route('/report', methods=['GET', 'POST'])
def report():

    error = request.args.get('error', None)
    if request.method == 'POST':
        a =backend.getreport(request.form['phonen'])
        b = backend.getseller(request.form['phonen'])
        max_amount = 0
        notsold = 0
        sold = 0
        if a[0] ==0:

            current_item =a[1]
            b = list(b[1])
            c=[]
            for i in current_item:
                i = list(i)
                if i[7] ==0:
                    i[7]="Not Sold"
                    notsold=notsold+1
                elif i[7]==1:
                    i[7] = "Sold"
                    max_amount =max_amount+i[4]
                    sold=sold+1
                elif i[7] == 2:
                    i[7] = "Paid"
                    sold=sold+1
                elif i[7] == 3:
                    i[7] = "Returned"
                c.append(i)
            b[2] = backend.phone_format(str(b[2])).replace("-"," ")
            pay = max_amount*7
            pay=pay/10
            if "."in str(pay):
                paya = str(pay).split(".")
                pay = paya[0]+"."+paya[1][:2]
            return render_template(
            "reporta.html",
            item = c,
            user =b,
            max = max_amount,
            sold=sold,
            notsold=notsold,
            payout = pay)
        else:
            error = a
    return render_template("report.html",error=error)

@app.route('/r', methods=['POST'])
def reportapi():

    pnum =request.json["phone"]
    b = backend.getseller(pnum)
    if b[1][8]:
        return(jsonify({"status":"Error: Report already generated for this user"}),418)
    a =backend.reporta(request)
    if a ==0:
        #return redirect(url_for("home",msg = "Changed all items sold to paid"))
        return(jsonify({"status":"done"}),200)
    return 404

@app.route('/print_report')
def print_report():

    phone = request.args.get('phone', None)
    if phone:
        a =backend.getreport(phone)
        b = backend.getseller(phone)
        max_amount = 0
        notsold = 0
        sold = 0
        if a[0] ==0:
            current_item =a[1]
            b = list(b[1])
            c=[]
            for i in current_item:
                i = list(i)
                if i[7] ==0:
                    i[7]="Not Sold"
                    notsold=notsold+1
                elif i[7]==1:
                    i[7] = "Sold"
                    max_amount =max_amount+i[4]
                    sold=sold+1
                elif i[7] == 2:
                    i[7] = "Paid"
                    sold=sold+1
                    max_amount =max_amount+i[4]
                elif i[7] == 3:
                    i[7] = "Returned"
                c.append(i)
            b[2] = backend.phone_format(str(b[2])).replace("-"," ")
            pay = max_amount*0.7
            if "."in str(pay):
                paya = str(pay).split(".")
                pay = paya[0]+"."+paya[1][:2]
            return render_template(
                "rec.html", 
                item = c,
                user =b,
                sold=sold,
                payout = pay,
                seller = b[3],
                phone = b[2],
                address=b[4])

    return redirect(url_for("report"))
@app.route('/print')
def print_api():

    return redirect(url_for("report"))

@app.route('/checkout')
def checkout():

    return render_template("checkout.html")
@app.route('/api/getitem')
def api_getitem():

    num = request.args.get('itemnum', None)
    a = backend.getitem(num)
    return({"res":a[0],"data":a[1]})
@app.route('/api/postitems', methods=['POST'])
def api_postitems():

    content = request.json
    a = backend.postitems(content,request)
    if a[0] == 0:
        return jsonify({"status":"updated"})
    elif a[0] ==1:
        return jsonify({"status":a[1]}),412
    else:
        return jsonify({"status":a[1]}),418

@app.route('/logs')
def logs():

    return render_template("logs.html")

@app.route('/api/getlog', methods=['POST'])
def api_getlog():

    a=backend.getlog(request.json["password"])
    if a[0]==1:
        return({"res":a[0],"data":a[1]})
    return(jsonify({"res":a[0],"data":a[1]}),418)


@app.route('/api/db')
def api_downloadlog():

    a = backend.getall()
    things = ["user","items","log"]
    count = 0
    for i in a:
        with open(f"./download/{things[count]}.csv", 'w', encoding="utf-8") as f:
            for k in i:
                add = "0"
                for j in k:
                    if j:
                        add=add+","+str(j)
                    else:
                        add=add+","+"NONE"
                f.write(add)
                f.write("\n")
        count = count+1
    #return send_from_directory(directory='logs')
    return render_template("down.html")
@app.route('/down/<filename>', methods=['GET', 'POST'])
def download(filename):

    if filename not in ["user.csv","items.csv","log.csv"]:
        return "File does not exist"
    try:
        return send_file(f"./download/{filename}")
    except FileNotFoundError:
        return "File does not exist"

@app.route("/download/database")
def download_db():

    return send_file("main.db")

@app.route("/admin")
def admin():

    return render_template("admin.html")

if __name__ == "__main__":
    app.run()
