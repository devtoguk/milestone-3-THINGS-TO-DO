from flask import Flask, jsonify, request, session, redirect
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

    def add_activity(self):
        # print(request.form)
        user_session = session.get("user")

        # Create the activity object
        #
        activity = {
            'title': request.form.get('title'),
            'shortDescr': request.form.get('short_descr'),
            'longDescr': request.form.get('long_descr'),
            'location': int(request.form.get('location')),
            'ageRange': request.form.get('age_range'),
            'category': request.form.getlist('category'),
            'online': bool(request.form.get('online')),
            'whenTodo': request.form.getlist('when_todo'),
            'keywords': request.form.get('keywords'),
            'additionalURL': request.form.get('additional_url'),
            'status': 0,
            'featured': False,
            'free': bool(request.form.get('free')),
            'userid': ObjectId(user_session['_id']['$oid']),
            'createdOn': datetime.datetime.now(),
        }

        # If location is 'Out & About' then add venue data
        #
        if int(request.form.get('location')) == 2:
            activity['venue'] = {
                'name': request.form.get('name'),
                'addressLines': request.form.get('address_lines'),
                'town': request.form.get('town').lower(),
                'county': request.form.get('county').lower(),
                'postcode': request.form.get('postcode'),
                'website': request.form.get('website'),
                'email': request.form.get('email'),
            }

        # Check if activity with same title already exists
        #
        if mongo.db.activities.find_one({'title': activity['title']}):
            return jsonify({'error': 'An activity already has that title'}), 400

        # Add activity into the database and return the activity object
        #
        if mongo.db.activities.insert_one(activity):
            activity_json_str = dumps(activity,
                                      json_options=RELAXED_JSON_OPTIONS)
            activity_json = json.loads(activity_json_str)
            return activity_json, 200

        return jsonify({'error': 'Activity submission failed'}), 400
