import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

from user import routes

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html",
                           page_title="Things to Do and Places to Go: Home page",
                           page_description="From small adventures at home, to big adventures on days out! Find something to do...",nav_link="Home")


@app.route("/dbtest/")
def dbtest():
    activities = list(mongo.db.activities.find())
    # print(activities)
    return render_template("dbtest.html", activities=activities)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
