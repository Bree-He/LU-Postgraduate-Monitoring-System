from flask import (redirect, render_template, request,
                   session, url_for, Response, make_response)
from main import app
from main.config import sendMail
from main.common import getCursor
import re
import bcrypt

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/loginuser", methods=['GET', 'POST'])
def loginuser():
    if request.method == 'POST':
        # get username from the login
        username = request.form.get('username')
        password = request.form.get('password')
        connection = getCursor()
        connection.execute("SELECT role, password, admin_flag  FROM user WHERE email_lu=%s", (username,)) 
        rows = connection.fetchall()
        if len(rows) > 0:
            role = rows[0][0]
            pw = rows[0][1]
            admin_flag = rows[0][2] #this is the status of account activation, 1 = activated, 0 = deactivated
            if admin_flag != 1:
                error = 'Your account is deactivated, please contact the administrator for assistance!'
                return render_template('login.html', error=error)
            elif bcrypt.checkpw(password.encode('utf-8'),pw.encode('utf-8')) != True:
                error = 'Incorrect username or password, please try again!'
                return render_template('login.html', error=error)
            # store username and role in session
            session['username'] = username
            session['role'] = role
            if role == 'Postgraduate Administrator':
                return redirect(url_for('admin.index'))
            elif role == 'Student':
                return redirect(url_for('student.index'))
            elif role == 'Supervisor':
                return redirect(url_for('supervisor.index')) 
            elif role == 'Convenor':
                return redirect(url_for('convenor.index'))
            elif role == 'Postgraduate Chair':
                return redirect(url_for('chair.index'))
        else:
            error = 'Incorrect username or password, please try again!'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    error = ''
    success = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        email = request.form['username']
        password = request.form['password']
        connection = getCursor()
        connection.execute('SELECT * FROM user WHERE email_lu = %s', (email,))
        account = connection.fetchone()
        # If account exists show error and validation checks
        if account:
            error = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            error = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]{8,12}', password):
            error = 'Your password must be 8-12 characters in length, containing numbers, upper and lower letters!'
        elif not email or not password:
            error = 'Please fill out the form!'
        else:
            # Account doesn't exists and the form data is valid, check if the email is register in Faculty of Environment, Society and Design
            connection.execute("SELECT email_lu FROM student WHERE email_lu=%s", (email,))
            account = connection.fetchone()
            if account is None:
                error = 'You are not a registered student in the Faculty of Environment, Society and Design!'
            else:
                #registered student checked, now insert new account into accounts table   
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                connection.execute('INSERT INTO USER (email_lu, role, password, admin_flag) \
                                    VALUES (%s, "Student", %s, "0")', (email, hashed))
                success = 'Register successfully, you will receive an email once the account is activated!'
                connection.execute("SELECT email_lu FROM staff WHERE role = 'Postgraduate Administrator'") 
                adminEmail = connection.fetchone()[0]
                emailTitle = 'New User Registered!'
                emailBody = "A new user register the PGD Monitor System today, please log in to the system to check!"
                sendMail(emailTitle, adminEmail, emailBody) #admin will receive email notification from the system when new student register
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        error = 'Please fill out the form!'
    return render_template('register.html', error=error, success=success)