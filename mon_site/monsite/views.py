from flask import Blueprint, render_template, session, request, redirect, url_for
from flask_login import login_required, current_user
from . models import Account
import psycopg2
views = Blueprint('views', __name__)

@views.route("/", methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        conn=psycopg2.connect('dbname=pythonlogin user=postgres password=030825 port=5432 host=localhost') 
        cur = conn.cursor()
        cur.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password,))
        account = cur.fetchone()
        if account:
            session['loggedin'] = True
            accout = Account.query.all()
            return redirect("/home")
        else:
            msg = 'Nom d\'utilisateur ou Mot de passe incorrect !'
            return render_template('index.html',msg=msg)

    return render_template("index.html")