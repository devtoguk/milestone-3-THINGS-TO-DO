from flask import jsonify, request, session, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
import json
import datetime
from flask_pymongo import PyMongo

mongo = PyMongo()


class User:

    def start_session(self, user):
        """Setup user session with the user object data

        :param user: object from mongoDB users collection
        :return: json object containing user data without password/favourites
        """
        del user['password']
        if 'favourites' in user:
            del user['favourites']
        session['logged_in'] = True
        # Convert user object to json
        user_json_str = dumps(user, json_options=RELAXED_JSON_OPTIONS)
        user_json = json.loads(user_json_str)
        session['user'] = user_json
        return user_json, 200

    def add_user(self):
        """Add new user to the database

        :return: start user session or registration failed
        """
        # Create the user object
        user = {
            'name': request.form.get('name'),
            'screenName': request.form.get('screen_name'),
            'email': request.form.get('email'),
            'postcode': request.form.get('postcode').lower(),
            'town': request.form.get('town').lower(),
            'county': request.form.get('county').lower(),
            'level': 0,
            'favourites': [],
            'password': request.form.get('password')
        }

        # Encrypt the password
        user['password'] = generate_password_hash(user['password'])

        # Check if user email address already exists
        if mongo.db.users.find_one({'email': user['email']}):
            return jsonify({'error': 'Email address already in use'}), 400

        # Add user into the database and return the user object
        if mongo.db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({'error': 'User registration failed'}), 400

    def logout(self):
        """Logout the user

        :return: redirect to the home page
        """
        session.clear()
        flash('You have been logged-out', 'info')
        return redirect(url_for('index'))

    def login_user(self):
        """Login the user

        :return: start user session or invalid login credentials
        """
        user = mongo.db.users.find_one({'email':  request.form.get('email')})
        if user and check_password_hash(
                    user['password'],
                    request.form.get('password')):
            return self.start_session(user)

        return jsonify({'error': 'Invalid user login credentials'}), 401


class Activity:

    def activity_object(self):
        """Create the activity object

        :return: activity object
        """
        user_session = session.get('user')
        activity = {
            'title': request.form.get('title').lower(),
            'shortDescr': request.form.get('shortDescr'),
            'longDescr': request.form.get('longDescr'),
            'location': int(request.form.get('location')),
            'ageRange': request.form.get('ageRange'),
            'category': request.form.getlist('category'),
            'online': int(request.form.get('online')),
            'whenTodo': request.form.getlist('whenTodo'),
            'status': 0,
            'featured': False,
            'freeTodo': int(request.form.get('freeTodo')),
            'userid': ObjectId(user_session['_id']['$oid']),
            'createdOn': datetime.datetime.now(),
        }

        # Add non-blank optional fields additionalURL & keywords
        if len(request.form.get('keywords')) > 0:
            activity['keywords'] = request.form.get('keywords')
        if len(request.form.get('additionalURL')) > 0:
            activity['additionalURL'] = request.form.get('additionalURL')

        # If location is 2 'At a Venue' then add venue data
        if int(request.form.get('location')) == 2:
            activity['venue'] = {
                'name': request.form.get('venue-name'),
                'address': request.form.get('venue-address'),
                'postcode': request.form.get('venue-postcode'),
            }
            if len(request.form.get('venue-email')) > 0:
                activity['venue']['email'] = request.form.get('venue-email')
            if len(request.form.get('venue-website')) > 0:
                activity['venue']['website'] = request.form.get(
                                               'venue-website')
        return activity

    def get_activity(self, activity_id):
        """Get activity from the database for edit or exist check

        :param activity_id: string
        :return: matching activity from the database
        """
        activity = mongo.db.activities.find_one({'_id': ObjectId(activity_id)})
        return activity

    def view_activity(self, activity_id):
        """Get activity from the database for viewing activity

        :param activity_id: string
        :return: matching activity from the database with user creation data
                 else None
        """
        find_activity = list(mongo.db.activities.aggregate(
            [
                {'$match': {'_id': ObjectId(activity_id)}},
                {'$lookup': {
                    'from': 'users',
                    'let': {'user_id': '$userid'},
                    'pipeline': [{
                        '$match': {'$expr': {'$eq': ['$_id', '$$user_id']}}
                    },
                        {'$project': {'password': 0, 'level': 0, '_id': 0}}
                    ],
                    'as': 'userInfo'
                }},
                {'$unwind': '$userInfo'}
            ]))
        if len(find_activity) > 0:
            activity = find_activity[0]
            return activity
        else:
            return None

    def add_activity(self):
        """Add activity to the database

        :return: Title exists, inserted ObjectId or submission failed
        """
        # Create the activity object
        activity = self.activity_object()
        # Check if activity with same title already exists
        if mongo.db.activities.find_one({'title': activity['title']}):
            flash(f'''Activity called "{ activity["title"] }"
                      already exists.''', 'error')
            return 'TITLE_EXISTS', 400

        # Add activity into the database and return the activity object
        insert_result = mongo.db.activities.insert_one(activity)
        if insert_result:
            flash(f'''Thank you...  "{ activity["title"] }"
                      activity submitted.''', 'info')
            return str(insert_result.inserted_id), 200

        flash('Activity submission failed', 'error')
        return jsonify({'error': 'Activity submission failed'}), 400

    def update_activity(self, activity_id):
        """Update existing activity in the database

        :param activity_id: string
        :return: success 200 or error 400
        """
        # Create the activity object
        activity = self.activity_object()
        # Remove userid & createdOn fields so we don't override creator info
        del activity['userid']
        del activity['createdOn']
        # Remove featured so the featured status is not changed back to false
        del activity['featured']

        # Update activity in the database and return the activity object
        if mongo.db.activities.update_one({'_id': ObjectId(activity_id)},
                                          {'$set': activity}):
            flash(f'"{ activity["title"] }" updated.', 'info')
            return jsonify({'success': 'Activity updated'}), 200

        flash('Activity update failed', 'error')
        return jsonify({'error': 'Activity update failed'}), 400
