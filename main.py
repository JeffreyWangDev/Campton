"""Main file for all code relating to the server"""
import sqlite3 as sl
import werkzeug
from flask import Flask,redirect,render_template,request,url_for,jsonify, send_file
#from backend import *
import backend
import make_db as backend_make
app = Flask(__name__)

@app.route('/goto', methods=['GET', 'POST'])
def goto():
    """
    Redirects to the specified route based on the 'place' query parameter.
    If 'place' is not provided or the route doesn't exist, it redirects to the 'home' route.

    Returns:
        Flask redirect response.
    """
    place = request.args.get('place', None)
    try:
        return redirect(url_for(place))
    except werkzeug.routing.exceptions.BuildError:
        return redirect(url_for("home"))

@app.route('/')
def home():
    """
    Renders the 'home.html' template with an optional 'msg' query parameter.

    Returns:
        Flask template render response.
    """
    msg = request.args.get('msg', None)
    return render_template("home.html",msg=msg)
@app.route('/make')
def make():
    """
    Initializes the database tables if they don't already exist.

    Returns:
        A simple confirmation message.
    """
    backend_make.make_database()

    return "Done"
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration. Accepts POST requests to register a new user.
    Displays a registration form and error messages on GET requests.

    Returns:
        - On successful registration, redirects to the 'home' route with a success message.
        - On GET request, renders the 'register.html' template with error and message.
    """
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
    """
    Handles user registration form submission. Goes to 'register' with error or success msg.

    Returns:
        Flask redirect response.
    """
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
    """
    Handles seller information display and form submission for seller search.

    Returns:
        - On successful seller info retrieval, renders the 'user.html' template with seller details.
        - On error or POST request, renders the 'user.html' template with error message.
    """
    error = None
    if request.method == 'POST':
        a = list(backend.getseller(request.form['phonenn']))
        if a[0]==0:
            aa = list(a[1])
            aa[2] = backend.phone_format(str(aa[2])).replace("-"," ")
            return render_template('user.html', user=aa)
        error = a[1]
    return render_template("user.html", error=error)

@app.route('/update', methods=['GET', 'POST'])
def update():
    """
    Handles user profile update. Accepts POST requests to update user information.
    Displays a user update form and error messages on GET requests.

    Returns:
        - On successful update, redirects to the 'home' route with a success message.
        - On GET request, renders the 'user.html' template for user profile update.
    """
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
    """
    Redirects to the 'seller' route.

    Returns:
        Flask redirect response.
    """
    return redirect(url_for('seller'))

@app.route('/newitem', methods=['GET', 'POST'])
def newitem():
    """
    Handles item creation. Accepts POST requests to add a new item.
    Displays an item creation form and error messages on GET requests.

    Returns:
        - On successful item creation, redirects to the 'home' route with a success message.
        - On GET request, renders the 'newitem.html' template with error and phone information.
    """
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
    """
    Handles item creation form submission. Redirects to 'newitem' with error or success msg.

    Returns:
        Flask redirect response.
    """
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
        return redirect(url_for('newitem', msg="Item added",phone=request.form['phonen']))
            #return redirect(url_for('newitem', msg="Item added"))
    return redirect(url_for('newitem', error=error))

@app.route('/item', methods=['GET', 'POST'])
def item():
    """
    Handles item information display and form submission for item search.

    Returns:
        - On successful item retrieval, renders the 'item.html' template with item details.
        - On error or POST request, renders the 'item.html' template with error message.
    """
    error = request.args.get('error', None)
    item_data = request.args.get('item', None)
    try:
        item_data = item_data.split("_____")
        if item_data[0] == "0":
            pass
        else:
            raise ValueError
    except (ValueError, IndexError, AttributeError):
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

        error = a[1]
    return render_template("item.html", error=error)

@app.route('/itemu', methods=[ 'POST'])
def itemu():
    """
    Handles item update form submission. Redirects to the 'item' route with error or success msg.

    Returns:
        Flask redirect response.
    """
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
    return None
@app.route('/report', methods=['GET', 'POST'])
def report():
    """
    Handles seller report generation and display. Accepts POST requests to generate reports.
    Displays a report form and error messages on GET requests.

    Returns:
        - On successful report gen, renders the 'reporta.html' template with seller/item info.
        - On error or POST request, renders the 'report.html' template with error message.
    """
    error = request.args.get('error', None)
    if request.method == 'POST':
        a = backend.getreport(request.form['phonen'])
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

        error = a
    return render_template("report.html",error=error)

@app.route('/r', methods=['POST'])
def reportapi():
    """
    Handles API requests to generate seller reports.

    Returns:
        - On successful report generation, returns a JSON response with a status message.
        - On error, returns a JSON response with an error status and code 418.
    """
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
    """
    Handles seller report printing.

    Returns:
        Renders the 'rec.html' template with seller and item details.
    """
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
    """
    Redirects to the 'report' route for report printing.

    Returns:
        Flask redirect response.
    """
    return redirect(url_for("report"))

@app.route('/checkout')
def checkout():
    """
    Renders the 'checkout.html' template.

    Returns:
        Flask template render response.
    """
    return render_template("checkout.html")
@app.route('/api/getitem')
def api_getitem():
    """
    Handles API requests to retrieve item details.

    Returns:
        - On successful item retrieval, returns a JSON response with item data.
        - On error, returns a JSON response with an error status and code 418.
    """
    num = request.args.get('itemnum', None)
    a = backend.getitem(num)
    return({"res":a[0],"data":a[1]})
@app.route('/api/postitems', methods=['POST'])
def api_postitems():
    """
    Handles API requests to post items.

    Returns:
        - On successful item update, returns a JSON response with a status message.
        - On error, returns a JSON response with an error status and code 412 or 418.
    """
    content = request.json
    a = backend.postitems(content,request)
    if a[0] == 0:
        return jsonify({"status":"updated"})
    if a[0] ==1:
        return jsonify({"status":a[1]}),412
    return jsonify({"status":a[1]}),418

@app.route('/logs')
def logs():
    """
    Renders the 'logs.html' template.

    Returns:
        Flask template render response.
    """
    return render_template("logs.html")

@app.route('/api/getlog', methods=['POST'])
def api_getlog():
    """
    Handles API requests to retrieve logs.

    Returns:
        - On successful log retrieval, returns a JSON response with log data.
        - On error, returns a JSON response with an error status and code 418.
    """
    a=backend.getlog(request.json["password"])
    if a[0]==1:
        return({"res":a[0],"data":a[1]})
    return(jsonify({"res":a[0],"data":a[1]}),418)


@app.route('/api/db')
def api_downloadlog():
    """
    Handles API requests to download database logs.

    Returns:
        Renders the 'down.html' template for download.
    """
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
    """
    Handles file download requests.

    Args:
        filename (str): Name of the file to be downloaded.

    Returns:
        - On success, serves the requested file for download.
        - On error (file not found), returns an error message.
    """
    if filename not in ["user.csv","items.csv","log.csv"]:
        return "File does not exist"
    try:
        return send_file(f"./download/{filename}")
    except FileNotFoundError:
        return "File does not exist"

@app.route("/download/database")
def download_db():
    """
    Handles database download requests.

    Returns:
        Serves the main database file for download.
    """
    return send_file("main.db")

@app.route("/admin")
def admin():
    """
    Renders the 'admin.html' template.

    Returns:
        Flask template render response.
    """
    return render_template("admin.html")

if __name__ == "__main__":
    app.run()
