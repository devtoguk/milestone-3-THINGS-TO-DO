from flask import Flask, render_template
from __main__ import app
from user.models import User


@app.route("/user/register/")
def register():
    return render_template("register.html")


@app.route("/user/adduser/", methods=["POST"])
def add_user():
    return User().add_user()


@app.route("/user/logout/")
def logout():
    return User().logout()
