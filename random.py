from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
  
  
app = Flask(__name__)
  
  
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'registration'
  
mysql = MySQL(app)

app.secret_key = ''
  
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'UserID' in request.form and 'UserPassword' in request.form:
        UserID = request.form['UserID']
        UserPassword = request.form['UserPassword']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE UserID = % s AND UserPassword = % s', (UserID, UserPassword, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['UserID'] = account['UserID']
            msg = 'Logged in successfully !'
            return render_template('home.html', msg = msg)
        else:
            msg = 'Incorrect userID / password !'
    return render_template('login3.html', msg = msg)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('UserID', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'UserID' in request.form and 'UserPassword' in request.form and 'Mobilenumber' in request.form :
        UserID = request.form['UserID']
        UserPassword = request.form['UserPassword']
        Mobilenumber = request.form['Mobilenumber']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE userID = % s', (UserID, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', UserID):
            msg = 'Invalid email address !'
        elif not UserID or not UserPassword or not Mobilenumber:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (UserID, UserPassword, Mobilenumber, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register3.html', msg = msg)

if __name__=='_main_':
    app.secret_key=''
    app.run(debug=True)