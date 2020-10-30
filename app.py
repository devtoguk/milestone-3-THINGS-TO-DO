import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
if os.path.exists("env.py"):
    import env

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html",
                           page_title="Things to Do and Places to Go: Home page",
                           page_description="From small adventures at home, to big adventures on days out! Find something to do...",nav_link="Home")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
