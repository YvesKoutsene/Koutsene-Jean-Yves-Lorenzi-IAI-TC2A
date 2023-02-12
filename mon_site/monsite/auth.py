from flask import Blueprint, render_template, request, redirect, url_for, session
import re
import psycopg2
auth = Blueprint('auth', __name__)
from .models import Account

@auth.route('/home')
def home():
        accout =''
        if request.method == 'POST' and 'email' in request.form:
                mail = request.form['email']
                conn=psycopg2.connect('dbname=pythonlogin user=postgres password=030825 port=5432 host=localhost')
                cur = conn.cursor()
                cur.execute('SELECT * FROM accounts WHERE email = %s', (mail,))
                accout = cur.fetchone()
                conn.close()
        return render_template ("home.html",accout=accout)

@auth.route('/register', methods=['GET', 'POST'])
def register():
        msg = ''
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form  and 'pass2' in request.form and 'email' in request.form:
                username = request.form['username']
                password = request.form['password']
                password2 = request.form['pass2']
                email = request.form['email']
                conn=psycopg2.connect('dbname=pythonlogin user=postgres password=030825 port=5432 host=localhost')
                cur = conn.cursor()
                cur.execute('SELECT * FROM accounts WHERE email = %s', (email,))
                account = cur.fetchone()

                if account:
                        msg = 'Desolé ce compte existe déja !'

                elif(password2 != password):
                        msg = "Les mots de passe ne sont pas conformes"
                        
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                        msg = 'Email invalide !'
                        
                elif not re.match(r'[A-Za-z0-9]+', username):
                        msg = 'Le nom d\'utilisateur doit pas contenir de chiffres !'
                        
                elif not username or not password or not email:
                        msg = 'Pardon veuillez remplir tout le fomrulaire!'
                        
                else:
                        cur.execute('INSERT INTO accounts(username, password, email) VALUES (%s, %s, %s)', (username, password, email,))
                        cur.close()
                        conn.commit()
                        msg = 'Enregistrer avec succès. Menant connectez-vous'        
        return render_template('register.html', msg=msg)

#@auth.route('/logout')
#def logout():
   #session.pop('loggedin', None)
   #return render_template("index.html")

@auth.route('/profile')
def profile():
        accout = ''
        if 'loggedin' in session:
                if request.method == 'POST' and 'email' in request.form:
                        mail = request.form['email']
                        conn=psycopg2.connect('dbname=pythonlogin user=postgres password=030825 port=5432 host=localhost')
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM accounts WHERE email = %s',(mail,))
                        accout = cur.fetchone()
                        conn.close()
                return render_template ("profile.html",accout=accout)

