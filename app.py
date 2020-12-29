import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from bson.objectid import ObjectId
from flask_uploads import configure_uploads, IMAGES, UploadSet
from werkzeug.exceptions import RequestEntityTooLarge
from models import mongo, User, Activity
from forms import ActivityForm
from consts import CATEGORIES
from image import resize_image
from functions import (
    set_imageURL, upload_file, check_activity_id)

if os.path.exists('env.py'):
    import env

app = Flask(__name__)


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
    """Resize and upload image to S3 Bucket

    :param data: image data
    :param filename: string
    """
    file_path = images.path(filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    # Save temporary image and resize
    image_folder = 'static/images/activities/'
    bucket_name = os.environ.get('S3_BUCKET_NAME')
    images.save(data, None, filename)
    resize_image(filename)

    # Upload image to AWS S3 bucket
    file_path = image_folder + filename
    upload_file(file_path, bucket_name, object_name=filename)


@app.errorhandler(404)
def page_unknown(e):
    return render_template(
        'error.html',
        error_message='Sorry we cannot locate that page.',
        error_code=e)


@app.errorhandler(413)
def too_large(e):
    return render_template(
        'error.html',
        error_message=('The file you chose was too large, '
                       'our gallery limit is 4mb.'),
        error_code=e)


@app.route('/')
def index():
    """
    Render Home page
    """
    return render_template(
        'index.html',
        page_title='Things to Do and Places to Go: Home page',
        page_description=('From small adventures at home, '
                          'to big adventures on days out! '
                          'Find something to do...'),
        nav_link='Home',
        categories=CATEGORIES)


@app.route('/about/')
def about():
    """
    Render About Us page
    """
    return render_template(
        'about.html',
        page_title='About Things to Do and Places to Go',
        page_description=('Find out a little more about the '
                          'activity website, Things to Do and '
                          'Places to Go.'),
        nav_link='About',
        categories=CATEGORIES)


@app.route('/search/', methods=['POST', 'GET'])
def search():
    """
    Render text search results
    """
    if request.method == "POST":
        search_text = request.form.get('search_text')
        activities = list(mongo.db.activities.find(
                          {'$text':
                              {'$search': search_text}}))
        total = len(activities)
        if total > 0:
            flash(f'''{total} result{"s" if total != 1 else ""}
                      for "{search_text}"''', 'info')

            # Set image URLs either no_image_yet or S3 bucket image
            for act in activities:
                act['imageURL'] = set_imageURL(act["_id"])

            return render_template(
                'results.html',
                page_title=('Things to Do and Places to Go: '
                            f'Search results for "{search_text}"'),
                activities=activities,
                categories=CATEGORIES)
        else:
            flash(f'No results for "{search_text}"', 'info')
            return redirect(url_for('index'))


@app.route('/category/<string:category>/', methods=['POST', 'GET'])
def category(category):
    """
    Show database results based on the selected category

    :param category: string
    :return: render results or redirect to home page
    """
    # Set default results flash message
    message = f'{category} Activities'

    if request.method == "GET":
        if category == 'All':
            activities = list(mongo.db.activities.find())
        elif category == 'Featured':
            activities = list(mongo.db.activities.find({'featured': True}))
        elif category == 'Recently Added':
            activities = list(mongo.db.activities.
                              find().sort('createdOn', -1).limit(6))
        elif category == 'Submitted':
            user_session = session.get('user')
            if user_session:
                userid = ObjectId(user_session['_id']['$oid'])
                activities = list(mongo.db.activities.
                                  find({'userid': ObjectId(userid)}).
                                  sort('createdOn', -1))
                message = 'Activities submitted by me'
            else:
                flash('You are not logged-in', 'error')
                return redirect(url_for('login'))

        elif category == 'Favourites':
            user_session = session.get('user')
            if user_session:
                userid = ObjectId(user_session['_id']['$oid'])
                # Get users favourites list
                user_data = list(mongo.db.users.
                                 find({'_id': ObjectId(userid)},
                                      {'_id': 0, 'favourites': 1}))
                user_favourites = user_data[0]['favourites']
                # Get activities which are in the users favourites list
                activities = list(mongo.db.activities.
                                  find({'_id': {'$in': user_favourites}}))
                message = 'My Favourite Activities'
            else:
                flash('You are not logged-in', 'error')
                return redirect(url_for('login'))

        else:
            activities = list(mongo.db.activities.find({'category': category}))
            total = len(activities)
            message = f'''{total} result{"s" if total != 1 else ""}
                          for [{category}]'''

        flash(message, 'info')

        # Set image URLs either no_image_yet or S3 bucket image
        for act in activities:
            act['imageURL'] = set_imageURL(act["_id"])

        return render_template(
            'results.html',
            page_title=(f'Things to Do and Places to Go: {message}'),
            activities=activities,
            nav_link='Activities',
            categories=CATEGORIES)

    return redirect(url_for('index'))


@app.route('/user/register/')
def register():
    """
    Render User Registration page
    """
    return render_template(
        'register.html',
        page_title=('Things to Do and Places to Go: User Registration'),
        nav_link='Login/Register',
        categories=CATEGORIES)


@app.route('/user/login/')
def login():
    """
    Render User Login page
    """
    return render_template(
        'login.html',
        page_title=('Things to Do and Places to Go: User Login'),
        nav_link='Login/Register',
        categories=CATEGORIES)


@app.route('/user/add_user/', methods=['POST'])
def add_user():
    """
    Attempt to add new user to database
    Called from javascript file
    """
    return User().add_user()


@app.route('/user/login_user/', methods=['POST'])
def login_user():
    """
    Attempt to login user
    Called from javascript file
    """
    return User().login_user()


@app.route('/user/logout/')
def logout():
    """
    Attempt to logout the user
    """
    return User().logout()


@app.route('/user/welcome/<string:user_status>/')
def welcome(user_status):
    """
    Setup user session and flash login message
    Called from javascript file

    :param user_status: string N for new user R for existing
    :return: redirect to home page
    """
    user_session = session.get('user')
    user_name = user_session.get('name', 0)
    if user_status == 'N':
        flash(f'''Welcome {user_name.title()},
                  thank you for registering.''', 'info')
    else:
        flash(f'{user_name.title()} logged-in.', 'info')

    return redirect(url_for('index'))


@app.route('/user/profile/')
def profile():
    """
    Render User Profile page
    """
    return render_template(
        'profile.html',
        page_title=('Things to Do and Places to Go: User Profile'),
        categories=CATEGORIES)


@app.route('/activity/submit/', methods=['GET', 'POST'])
def submit_activity():
    """
    Submit activity

    Render activity form
    Check form is valid and save to the database
    """
    if session.get('user') is None:
        flash('You must be logged-in to submit an Activity', 'error')
        return redirect(url_for('login'))

    form = ActivityForm()

    if form.validate_on_submit():
        td = form.venue.data
        del td['location']
        result = Activity().add_activity()
        activity_id = result[0]
        if result[0] != 'TITLE_EXISTS':
            if form.image.data:
                save_image(form.image.data, activity_id + '.jpg')

            return redirect(url_for('index'))

        form.title.errors.append('An activity with this name already exists')

    elif request.method == 'POST':
        flash('Please correct form errors below', 'error')

    return render_template(
        'activity_form.html', form=form,
        page_title=('Things to Do and Places to Go: Submit new Activity'),
        form_title='Add an Activity',
        nav_link='Submit_Activity',
        categories=CATEGORIES)


@app.route('/activity/edit/<string:activity_id>/', methods=['GET', 'POST'])
def edit_activity(activity_id):
    """
    Edit activity

    Render activity form
    Check form is valid and save to the database

    :param activity_id: string
    :return: redirect to home page
    """
    if session.get('user') is None:
        flash('You must be logged-in to edit an Activity', 'error')
        return redirect(url_for('login'))
    else:
        user_session = session.get("user")

    if check_activity_id(activity_id):
        activity_data = Activity().get_activity(activity_id)

        if activity_data is None:
            flash('Activity not found', 'error')
            return redirect(url_for('index'))

        users_level = user_session.get('level', 0)
        # Check user owns activity or user level is 1-moderator or 7-admin
        if (ObjectId(user_session['_id']['$oid']) !=
            ObjectId(activity_data['userid'])) and (
                users_level != 1 and users_level != 7):
            flash(f'''You cannot edit the activity "
                      {activity_data["title"]}"''', 'error')
            return redirect(url_for('index'))

        # Set imageURL for preview image
        imageURL = set_imageURL(activity_id)

        # Check form isn't too large (image data size)
        try:
            form = ActivityForm(data=activity_data)
        except RequestEntityTooLarge:
            flash('Chosen file too large, limit is 4mb', 'error')
            form = ActivityForm(data=activity_data)
        else:
            form.imageId.data = activity_id

            if form.validate_on_submit():
                # Remove venue location field as not required for database
                td = form.venue.data
                del td['location']

                if form.image.data:
                    save_image(form.image.data, activity_id + '.jpg')

                Activity().update_activity(activity_id)
                return redirect(url_for('index'))

            elif request.method == 'POST':
                flash('Please correct form errors below', 'error')

        return render_template(
            'activity_form.html', form=form,
            page_title=('Things to Do and Places to Go: Edit Activity'),
            form_title='Edit Activity',
            imageURL=imageURL,
            categories=CATEGORIES)
    else:
        return redirect(url_for('index'))


@app.route('/activity/view/<string:activity_id>/')
def view_activity(activity_id):
    """
    View activity

    :param activity_id: string
    :return: Render activity view or redirect to home page
    """
    # Check if activity_id is a valid ObjectId and exists in DB
    if check_activity_id(activity_id):
        activity_data = Activity().view_activity(activity_id)
        if activity_data is None:
            flash('Activity not found', 'error')
            return redirect(url_for('index'))

        # Set imageURL for activity image
        activity_data['imageURL'] = set_imageURL(activity_id)
        user_session = session.get('user')
        # Check if a user is logged-in
        if user_session:
            userid = ObjectId(user_session['_id']['$oid'])
            user_data = list(
                mongo.db.users.find({'_id': ObjectId(userid)},
                                    {'_id': 0, 'favourites': 1}))
            # Check if activity is in current users favourites
            if 'favourites' in user_data[0]:
                user_favourites = user_data[0]['favourites']
                if ObjectId(activity_id) in user_favourites:
                    activity_data['inUsersFavourites'] = 'Y'
                else:
                    activity_data['inUsersFavourites'] = 'N'
            else:
                # Current users favourites are empty
                activity_data['inUsersFavourites'] = 'N'
        else:
            # User is not logged-in
            activity_data['inUsersFavourites'] = 'U'

        return render_template(
            'activity.html',
            page_title=('Things to Do and Places to Go: Activity View'),
            activity=activity_data,
            nav_link='Activities',
            categories=CATEGORIES)
    else:
        return redirect(url_for('index'))


@app.route('/activity/favourite/<string:activity_id>/<string:action>/')
def favourite_activity(activity_id, action):
    """
    Add or remove activity from users Activity Favourites

    :param activity_id: string
    :param action: string '0' remove  '1' add
    :return: Render activity view or redirect to home page
    """
    # Check if activity_id is a valid ObjectId
    if not check_activity_id(activity_id):
        return redirect(url_for('index'))

    # Check if activity_id exists in mongoDB
    if not Activity().get_activity(activity_id):
        flash('Activity not found', 'error')
        return redirect(url_for('index'))

    user_session = session.get('user')
    # Check if a user is logged-in and set action variables
    if user_session:
        userid = ObjectId(user_session['_id']['$oid'])
        if action == '0' or action == '1':
            if action == '0':
                mongo_operator = '$pull'
                message = 'removed from'
            else:
                mongo_operator = '$push'
                message = 'added to'

            # Add / Remove activity_id from users favourites
            if mongo.db.users.update_one(
                {"_id": ObjectId(userid)},
                    {mongo_operator: {'favourites': ObjectId(activity_id)}}):
                flash(f'Activity {message} your Activity Favourites', 'info')
                return redirect(url_for(
                    'view_activity',
                    activity_id=activity_id))
            else:
                flash('Favourites update failed', 'error')
        else:
            flash('Favourites update operation invalid', 'error')
    else:
        flash('You must be logged-in to use Favourites', 'error')
        return redirect(url_for('login'))

    return redirect(url_for('index'))


@app.route('/form/cancel/<message>/')
def cancel_form(message):
    """
    Display form cancel message

    :param message: string
    :return: Redirect to home page
    """
    if message != 'None':
        flash(f'{message} cancelled', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
