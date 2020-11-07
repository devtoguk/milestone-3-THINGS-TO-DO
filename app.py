import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from functools import wraps

if os.path.exists('env.py'):
    import env

app = Flask(__name__)


# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*arg, **kwargs):
        if 'logged_in' in session:
            return f(*arg, **kwargs)
        else:
            return redirect('/')

    return wrap


# Routes
from user import routes

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html',
                           page_title='Things to Do and Places to Go: Home page',
                           page_description='From small adventures at home, to big adventures on days out! Find something to do...',nav_link='Home')


@app.route('/dbtest/')
def dbtest():
    activities = list(mongo.db.activities.find())
    # print(activities)
    return render_template('dbtest.html', activities=activities)


@app.route('/activity/')
@login_required
def activity():
    return render_template('activity.html')


@app.route('/search/', methods=['POST', 'GET'])
def search():
    if request.method == "POST":
        search_phrase = request.form.get('search_text')
        activities = list(mongo.db.activities.find({'$text':
                                                {'$search': search_phrase}}))
        return render_template('results.html',
                            results_type="text",
                            search_phrase=search_phrase, 
                            activities=activities)

    return render_template('index.html')
    

@app.route('/category/<string:category>/', methods=['POST', 'GET'])
def category(category):
    if request.method == "GET":
        print(category)
        cato = str(category)
        activities = list(mongo.db.activities.find({ 'category': category }))

        return render_template('results.html',
                            results_type="category",
                            search_category=category, 
                            activities=activities)
    
    return render_template('index.html')
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
