from types import resolve_bases
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from flask import request, jsonify, make_response, redirect, current_app
from sqlalchemy.exc import SQLAlchemyError

from bolo.auth import auth
from bolo.models import User, db


@auth.route('', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']

        user = User(username=username, pwd=password)
        try:
            db.session.add(user)
            db.session.commit()

            response = redirect(f"{current_app.config['BASE_URL']}/broadcast")
            return response

        except SQLAlchemyError:
            response = jsonify({
                "status": "fail",
                "message": "An unexpected error has occurred."
            })
            response = make_response(response)

            return response

    if request.method == 'GET':
        _users = User.query.all()

        users = []
        for user in _users:
            users.append({
                "id": user.id,
                "username": user.username
            })
        response = jsonify(users)
        return response
