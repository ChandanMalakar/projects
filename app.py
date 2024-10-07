from flask import Flask, render_template, request, redirect, session, json
from db import Database
import os
from waitress import serve

app = Flask(__name__)
app.secret_key = '1lkdf75gh49cm1603rm04'
dbo = Database()


__name__ == "__main__"



with open('users.json', 'r') as f:
    user_data = json.load(f)

@app.route('/')
def index():
    if 'user_email' not in session:  # Check if user is logged in
        return redirect('/login')
    return  render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('signup.html')


@app.route('/perform_registration',methods=['post'])
def perform_registration():
    if request.method == 'POST':
        name = request.form.get('user_ka_name')
        email = request.form.get('user_ka_email')
        password = request.form.get('user_ka_password')
        response = dbo.insert(name,email,password)
        if response:
            return render_template('login.html', message="Registration Successful. Kindly login to proceed", color='green') 
        else:
            return render_template('signup.html', message="E-mail already exits", color='red')
    return render_template('signup.html')
    
@app.route('/perform_login', methods=['post'])
def perform_login():
    if request.method == 'POST':
        email = request.form.get('user_ka_email')
        password = request.form.get('user_ka_password')
        response = dbo.search(email,password)
        if response:
            session['user_email'] = email
            return redirect('/profile')
        else:
            return render_template('login.html', message='Invalid email/password', color='red')
    return render_template('login.html')


@app.route('/profile')
def profile():
    if 'user_email' not in session:  # Check if user is logged in
        return redirect('/login')
    user_info = user_data.get(session['user_email'])
    return render_template('index.html', user_info=user_info)

@app.route('/ner')
def ner():
    if 'user_email' not in session:  # Check if user is logged in
        return redirect('/login')
    return render_template('ner.html')

@app.route('/aboutme')
def aboutme():
    if 'user_email' not in session:  # Check if user is logged in
        return redirect('/login')
    return render_template('about-me.html')

@app.route('/contact')
def contact():
    if 'user_email' not in session:  # Check if user is logged in
        return redirect('/login')
    return render_template('contact.html')

@app.route('/project')
def project():
    if 'user_email' not in session:  # Check if user is logged in
        return redirect('/login')
    return render_template('project.html')

@app.route('/logout')
def logout():
    session.pop('user_email', None)  # Remove user ID from session
    return render_template('login.html', message='Successfully Logged Out', color='green')

app.run()