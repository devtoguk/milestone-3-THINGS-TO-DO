from flask import Flask, jsonify


class User:

    def add_user(self):

        user = {
            "_id": "",
            "name": "",
            "email": "",
            "password": ""
        }

        return jsonify(user),200
