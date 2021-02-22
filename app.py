from flask import Flask,render_template,url_for,redirect,request,flash,session
from flask_mysqldb import MySQL
import MySQLdb.cursors 

app=Flask(__name__)

app.secret_key = 'your secret key'
#MYSQL CONNECTION
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="mydb"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)


#Login Page
@app.route('/')
@app.route("/Login", methods =['GET','POST'])
def Login():
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM manager WHERE username = % s AND password = % s', (username, password)) 
        account = cursor.fetchone() 
        if account: 
            session['loggedin'] = True
            session['id'] = account['id'] 
            session['username'] = account['username'] 
            msg = 'Logged in successfully !'
            con=mysql.connection.cursor()
            sql="SELECT * FROM products"
            con.execute(sql)
            res=con.fetchall()
            return render_template("overview.html",datas=res)

            
        else: 
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

#Logout Page
@app.route('/logout')
def Logout():
   # Remove session data
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('Login'))  


#Overview Page
@app.route('/overview')
def Overview():
        con=mysql.connection.cursor()
        sql="SELECT * FROM products"
        con.execute(sql)
        res=con.fetchall()
        return render_template("overview.html",datas=res)  

#Product Page
@app.route('/Product')
def Product():
    con=mysql.connection.cursor()
    sql="SELECT * FROM products"
    con.execute(sql)
    res=con.fetchall()
    return render_template("Product.html",datas=res)


#Add Product Page
@app.route("/addProduct",methods=['GET','POST'])
def addProduct():
    if request.method=='POST':
        product=request.form['product']
        quantity=request.form['quantity']
        con=mysql.connection.cursor()
        sql="insert into products (Product,Quantity) value (%s,%s)"
        con.execute(sql,[product,quantity])
        mysql.connection.commit()
        con.close()
        flash('Product Details Added')        
        return redirect(url_for("Product"))
    return render_template('addProduct.html')

#Edit Product Page
@app.route("/editDetails/<string:id>",methods=['GET','POST'])
def editDetails(id):
    con=mysql.connection.cursor()
    if request.method=='POST':
        product=request.form['product']
        quantity=request.form['quantity']
        sql="update products set Product=%s,Quantity=%s where Id=%s"
        con.execute(sql,[product,quantity,id])
        mysql.connection.commit()
        con.close()
        flash('Product Detail Updated')
        return redirect(url_for("Product"))
        con=mysql.connection.cursor()
        
    sql="select * from products where Id=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template('editDetails.html',datas=res)    

#Delete Product page
@app.route("/deleteProducts/<string:id>",methods=['GET','POST'])
def deleteProducts(id):
    con=mysql.connection.cursor()
    sql="delete from products where Id=%s"
    con.execute(sql,id)
    mysql.connection.commit()
    con.close()
    flash('Product Details Deleted')
    return redirect(url_for("Product"))  
   




if(__name__=='__main__'):
        app.run(debug=True)
 