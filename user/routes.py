from flask import Flask, render_template
from __main__ import app
from user.models import User


@app.route('/user/register/')
def register():
    return render_template('register.html')


@app.route('/user/login/')
def login():
    return render_template('login.html')


@app.route('/user/add_user/', methods=['POST'])
def add_user():
    return User().add_user()


@app.route('/user/login_user/', methods=['POST'])
def login_user():
    return User().login_user()


@app.route('/user/logout/')
def logout():
    return User().logout()