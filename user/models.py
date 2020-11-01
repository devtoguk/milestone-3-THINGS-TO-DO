from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from app import mongo

class User:

    def add_user(self):
        print(request.form)

        # Create the user object
        user = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "password": request.form.get("password")
        }

        # Encrypt the password
        user['password'] = generate_password_hash(user['password'])

        # Check if user email address already exists
        if mongo.db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400

        # Add user into the database and return the user object
        if mongo.db.users.insert_one(user):
            json_str = dumps(user, json_options=RELAXED_JSON_OPTIONS)
            return json_str, 200

        return jsonify({"error": "User registration failed"}), 400
