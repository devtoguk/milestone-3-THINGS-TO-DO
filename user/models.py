from flask import Flask, jsonify, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
import json
from app import mongo


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
            'email': request.form.get('email'),
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
