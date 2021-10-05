import re
from types import MethodDescriptorType
from flask import Flask, render_template, session, redirect, request
from loginandregistration_app import app
from loginandregistration_app.models.login import Login
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html')

@app.route('/user')
def user():
    if not session:
        return redirect ('/')
    data = session['userid']
    submission = Login.getsubmission(data)
    print ("THIS IS SUB", submission[0], "DATA", data)
    return render_template('user.html', submission = submission[0])

@app.route('/register', methods=['POST'])
def register():
    if not Login.register_validation(request.form):
        return redirect ('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'password' : pw_hash,
        'email' : request.form['email'],
        'age' : request.form['age']
        }
    newUser = Login.register(data)
    session['userid'] = newUser
    return redirect ('/user')

@app.route('/login', methods=['POST'])
def login():
    if not Login.login_validation(request.form):
        return redirect ('/')
    return redirect ('/user')

@app.route('/logout', methods=['GET'])
def restart():
    session.clear()
    return redirect('/')