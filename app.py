import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from bson.objectid import ObjectId
from functools import wraps
from flask_uploads import configure_uploads, IMAGES, UploadSet
from werkzeug.exceptions import RequestEntityTooLarge

from models import mongo, User, Activity
from forms import EditActivityForm, AddActivityForm
from consts import CATEGORIES
from image import resize_image
# import logging
# import boto3
# from botocore.exceptions import ClientError
from functions import (
    set_imageURL, create_presigned_url,
    upload_file)

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

app.config['UPLOADED_FILES_DEST'] = os.getcwd()
app.config['UPLOADS_DEFAULT_DEST'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

images = UploadSet('activities', IMAGES)
configure_uploads(app, images)


def save_image(data, filename):
    print(f'Trying to save image: {filename}')
    # Remove old file
    file_path = images.path(filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    # s3 = boto3.resource('s3')
    # print('Buckets:')
    # for bucket in s3.buckets.all():
    #     print(bucket.name)

    # Save and resize temporary image
    image_folder = 'static/images/activities/'
    bucket_name = os.environ.get('S3_BUCKET_NAME')

    images.save(data, None, filename)
    resize_image(filename)

    print(f'Filename: {filename}')
    file_path = image_folder + filename
    print(f'File-path: {file_path}')
    # Upload image to AWS S3
    # upload_file(data, bucket_name, object_name=filename)
    upload_file(file_path, bucket_name, object_name=filename)
    myURL = create_presigned_url(bucket_name,
                                 filename, expiration=880)

    print(f'My URL: {myURL}')


# @app.errorhandler(404)
# def page_unknown(e):
#     print(f'Error is: {e}')
#     return render_template('error.html',
#                            error_message='Sorry we cannot locate that page.',
#                            error_code=404)


@app.errorhandler(413)
def too_large(e):
    print(f'Error is: {e}')
    return render_template('error.html',
                           error_message='The file you chose was too large, our gallery limit is 2mb.',
                           error_code=413)


@app.route('/')
def index():
    return render_template('index.html',
                           page_title='Things to Do and Places to Go: Home page',
                           page_description='From small adventures at home, to big adventures on days out! Find something to do...',nav_link='Home',
                           categories=CATEGORIES)


@app.route('/about/')
def about():
    activities = list(mongo.db.activities.find())
    return render_template('about.html', activities=activities,
                           nav_link='About',
                           categories=CATEGORIES)


@app.route('/dbtest/')
def dbtest():
    activities = list(mongo.db.activities.find())
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
        search_text = request.form.get('search_text')
        activities = list(mongo.db.activities.find({'$text':
                                                {'$search': search_text}}))
        total = len(activities)
        if total > 0:
            flash(f'{total} result{"s" if total != 1 else ""} for "{search_text}"', 'info')

            for act in activities:
                act['imageURL'] = set_imageURL(act["_id"])

            return render_template('results.html',
                                   activities=activities,
                                   categories=CATEGORIES)
        else:
            flash(f'No results for "{search_text}"', 'error')
            return redirect(url_for('index'))


@app.route('/category/<string:category>/', methods=['POST', 'GET'])
def category(category):
    if request.method == "GET":
        if category == 'All':
            activities = list(mongo.db.activities.find())
        elif category == 'Featured':
            activities = list(mongo.db.activities.find({'featured': True}))
        else:
            activities = list(mongo.db.activities.find({'category': category}))

        total = len(activities)
        flash(f'{total} result{"s" if total != 1 else ""} for [{category}]', 'info')

        for act in activities:
            act['imageURL'] = set_imageURL(act["_id"])

        return render_template('results.html',
                               activities=activities,
                               nav_link='Activities',
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


@app.route('/user/welcome/')
def welcome():
    user_session = session.get('user')
    print(user_session)
    user_name = user_session.get('name', 0)
    flash(f'Welcome {user_name.title()}, thank you for registering.', 'info')
    return redirect(url_for('index'))


@app.route('/user/logged-in/')
def logged_in():
    user_session = session.get('user')
    print(user_session)
    user_name = user_session.get('name', 0)
    flash(f'{user_name.title()} logged-in.', 'info')
    return redirect(url_for('index'))


@app.route('/user/profile/')
def profile():
    return render_template('profile.html',
                           categories=CATEGORIES)


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
        activity_id = result[0]
        # print(f'New ID is: {activity_id}')
        if result[0] == 'TITLE_EXISTS':
            form.title.errors.append('An activity with this name already exists')
            return render_template('activity_form.html', form=form,
                                   form_title='Add an Activity',
                                   nav_link='Submit_Activity',
                                   categories=CATEGORIES)
        else:
            if form.image.data:
                save_image(form.image.data, activity_id + '.jpg')

        return redirect(url_for('index'))
    elif request.method == 'POST':
        print('Post with Errors!')
        flash('Please correct form errors below', 'error')

    return render_template('activity_form.html', form=form,
                           form_title='Add an Activity',
                           nav_link='Submit_Activity',
                           categories=CATEGORIES)


@app.route('/activity/edit/<string:activity_id>/', methods=['GET', 'POST'])
def edit_activity(activity_id):

    if session.get('user') is None:
        flash('You must be logged-in to edit an Activity', 'error')
        return redirect('/user/login/')
    else:
        user_session = session.get("user")

    activity_data = Activity().get_activity(activity_id)

    if activity_data is None:
        flash('Activity not found', 'error')
        return redirect(url_for('index'))

    users_level = user_session.get('level', 0)
    # Check if activity belongs to a user or if they are 1-moderator or 7-admin
    #
    if ObjectId(user_session['_id']['$oid']) != ObjectId(activity_data['userid']) and users_level != 1 and users_level != 7:
        flash(f'You cannot edit the activity "{activity_data["title"]}"',
              'error')
        return redirect(url_for('index'))

    # set current imageURL
    imageURL = set_imageURL(activity_id)

    try:
        form = EditActivityForm(data=activity_data)
    except RequestEntityTooLarge as e:
        flash('Chosen file too large, limit is 4mb', 'error')
        form = EditActivityForm(data=activity_data)
    else:
        form.imageId.data = activity_id

        if form.validate_on_submit():
            td = form.venue.data
            del td['location']
            # print(form.image.data)
            if form.image.data:
                if form.image.data:
                    save_image(form.image.data, activity_id + '.jpg')

            print(f'We were editing activity: {activity_id}')
            result = Activity().update_activity(activity_id)
            print(result)
            return redirect(url_for('index'))
        elif request.method == 'POST':
            print('Post with Errors!')
            flash('Please correct form errors below', 'error')

    return render_template('activity_form.html', form=form,
                           form_title='Edit Activity',
                           imageURL=imageURL,
                           categories=CATEGORIES)


@app.route('/activity/view/<string:activity_id>/')
def view_activity(activity_id):
    activity_data = Activity().get_activity(activity_id)
    if activity_data is None:
        flash('Activity not found', 'error')
        return redirect(url_for('index'))

    activity_data['imageURL'] = set_imageURL(activity_id)
    return render_template('activity.html',
                           activity=activity_data,
                           nav_link='Activities',
                           categories=CATEGORIES)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
