from flask import Flask, jsonify, request, session, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
import json
import datetime
from flask_pymongo import PyMongo

mongo = PyMongo()


class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        user_json_str = dumps(user, json_options=RELAXED_JSON_OPTIONS)
        user_json = json.loads(user_json_str)
        session['user'] = user_json
        # return user_json_str, 200
        return user_json, 200

    def add_user(self):
        print(request.form)

        # Create the user object
        user = {
            'name': request.form.get('name'),
            'screenName': request.form.get('screen_name'),
            'email': request.form.get('email'),
            'postcode': request.form.get('postcode').lower(),
            'town': request.form.get('town').lower(),
            'county': request.form.get('county').lower(),
            'level': 0,
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
            # json_str = dumps(user, json_options=RELAXED_JSON_OPTIONS)
            # return json_str, 200

        return jsonify({'error': 'User registration failed'}), 400

    def logout(self):
        session.clear()
        return redirect('/')

    def login_user(self):
        user = mongo.db.users.find_one({'email':  request.form.get('email')})

        if user and check_password_hash(user['password'], request.form.get('password')):
            return self.start_session(user)

        return jsonify({'error': 'Invalid user login credentials'}), 401


class Activity:

    def activity_object(self):
        user_session = session.get("user")
        activity = {
            'title': request.form.get('title'),
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
        #
        if len(request.form.get('keywords')) > 0:
            activity['keywords'] = request.form.get('keywords')
        if len(request.form.get('additionalURL')) > 0:
            activity['additionalURL'] = request.form.get('additionalURL')
        
        # If location is 'Out & About' then add venue data
        #
        if int(request.form.get('location')) == 2:
            activity['venue'] = {
                'name': request.form.get('venue-name'),
                'address': request.form.get('venue-address'),
                'postcode': request.form.get('venue-postcode'),
            }
            if len(request.form.get('venue-email')) > 0:
                activity['venue']['email'] = request.form.get('venue-email')
            if len(request.form.get('venue-website')) > 0:
                activity['venue']['website'] = request.form.get('venue-website')
        return activity

    def get_activity(self, activity_id):
        # print(f'Model - {activity_id}')
        activity = mongo.db.activities.find_one({'_id': ObjectId(activity_id)})
        print(f'Data: {activity}')
        # flash(f'Found activity called id "{ activity_id }" OK.', 'info')
        return activity

    def add_activity(self):
        # user_session = session.get("user")

        # Create the activity object
        #
        activity = self.activity_object()
        # Check if activity with same title already exists
        #
        if mongo.db.activities.find_one({'title': activity['title']}):
            flash(f'Activity called "{ activity["title"] }" already exists.', 'error')
            return 'TITLE_EXISTS', 400

        # Add activity into the database and return the activity object
        #
        if mongo.db.activities.insert_one(activity):
            activity_json_str = dumps(activity,
                                      json_options=RELAXED_JSON_OPTIONS)
            activity_json = json.loads(activity_json_str)
            flash(f'Thank you...  "{ activity["title"] }" activity submitted.', 'info')

            return activity_json, 200

        flash('Activity submission failed', 'error')
        return jsonify({'error': 'Activity submission failed'}), 400

    def update_activity(self, activity_id):
        user_session = session.get("user")

        # Create the activity object
        #
        activity = self.activity_object()
        # Remove user id field so we don't override the creator
        del activity['userid']
        # Update activity in the database and return the activity object
        #
        print(f'About to update: {activity_id}')
        if mongo.db.activities.update_one({"_id": ObjectId(activity_id)},
                                          {"$set": activity}):
            activity_json_str = dumps(activity,
                                      json_options=RELAXED_JSON_OPTIONS)
            activity_json = json.loads(activity_json_str)
            flash(f'"{ activity["title"] }" activity updated.', 'info')

            return activity_json, 200

        flash('Activity update failed', 'error')
        return jsonify({'error': 'Activity update failed'}), 400
