import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from bson.objectid import ObjectId
from functools import wraps

from models import mongo, User, Activity
from forms import EditActivityForm, AddActivityForm
from consts import CATEGORIES, WHEN_TODO

if os.path.exists('env.py'):
    import env

app = Flask(__name__)


# Decorators
#
def login_required(f):
    @wraps(f)
    def wrap(*arg, **kwargs):
        if 'logged_in' in session:
            return f(*arg, **kwargs)
        else:
            return redirect('/')

    return wrap


app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET_KEY')

mongo.init_app(app)


@app.route('/')
def index():
    # flash('Test flash message', 'info')
    return render_template('index.html',
                           page_title='Things to Do and Places to Go: Home page',
                           page_description='From small adventures at home, to big adventures on days out! Find something to do...',nav_link='Home',
                           categories=CATEGORIES)


@app.route('/dbtest/')
def dbtest():
    activities = list(mongo.db.activities.find())
    # print(activities)
    return render_template('dbtest.html', activities=activities,
                           categories=CATEGORIES)


@app.route('/activity/')
@login_required
def activity():
    return render_template('activity.html',
                           categories=CATEGORIES)


@app.route('/search/', methods=['POST', 'GET'])
def search():
    if request.method == "POST":
        search_phrase = request.form.get('search_text')
        activities = list(mongo.db.activities.find({'$text':
                                                {'$search': search_phrase}}))
        return render_template('results.html',
                               results_type="text",
                               search_phrase=search_phrase,
                               activities=activities,
                               categories=CATEGORIES)

    return render_template('index.html')


@app.route('/category/<string:category>/', methods=['POST', 'GET'])
def category(category):
    if request.method == "GET":
        activities = list(mongo.db.activities.find({'category': category.lower()}))

        return render_template('results.html',
                               results_type="category",
                               search_category=category,
                               activities=activities,
                               categories=CATEGORIES)

    return render_template('index.html')


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


@app.route('/activity/submit/', methods=['GET', 'POST'])
def submit_activity():

    if session.get('user') is None:
        flash('You must be logged-in to submit an Activity', 'error')
        return redirect('/user/login/')

    form = AddActivityForm()

    if form.validate_on_submit():
        # flash(f'Activity {form.title.data} created.', 'info')
        td = form.venue.data
        del td['location']
        # result = td.pop('location', None)
        # print(f'Result = {result}')
        # print(td)
        result = Activity().add_activity()
        # print(result)
        if result[0] == 'TITLE_EXISTS':
            form.title.errors.append('An activity with this name already exists')
            return render_template('activity_form.html', form=form,
                                   form_title='Add an Activity',
                                   categories=CATEGORIES)

        return redirect(url_for('index'))
    elif request.method == 'POST':
        print('Post with Errors!')
        flash('Please correct form errors below', 'error')

    return render_template('activity_form.html', form=form,
                           form_title='Add an Activity',
                           categories=CATEGORIES)


@app.route('/activity/edit/<string:activity_id>/', methods=['GET', 'POST'])
def edit_activity(activity_id):

    if session.get('user') is None:
        flash('You must be logged-in to edit an Activity', 'error')
        return redirect('/user/login/')
    else:
        user_session = session.get("user")

    activity_data = Activity().get_activity(activity_id)
    users_level = user_session.get('level', 0)
    # Check if activity belongs to a user or if they are 1-moderator or 7-admin
    #
    if ObjectId(user_session['_id']['$oid']) != ObjectId(activity_data['userid']) and users_level != 1 and users_level != 7:
        flash(f'You cannot edit the activity "{activity_data["title"]}"',
              'error')
        return redirect(url_for('index'))

    # print(f'From route: {activity_data}')

    form = EditActivityForm(data=activity_data)

    if form.validate_on_submit():
        td = form.venue.data
        del td['location']
        print(f'We were editing activity: {activity_id}')
        result = Activity().update_activity(activity_id)
        print(result)
        return redirect(url_for('index'))
    elif request.method == 'POST':
        print('Post with Errors!')
        flash('Please correct form errors below', 'error')

    return render_template('activity_form.html', form=form,
                           form_title='Edit Activity',
                           categories=CATEGORIES)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
