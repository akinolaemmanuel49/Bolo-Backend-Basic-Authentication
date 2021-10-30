from flask import json, request, jsonify, make_response
from flask.globals import g
from sqlalchemy.exc import SQLAlchemyError

from bolo.broadcast import broadcast
from bolo.models import User, Broadcast, db
from bolo.helpers import basic_auth


@broadcast.route('', methods=['GET', 'POST'])
@basic_auth.login_required
def create_broadcast():
    if request.method == 'POST' and request.json['message']:
        message = request.json['message']
        broadcast = Broadcast(message=message, user=basic_auth.current_user())

        try:
            db.session.add(broadcast)
            db.session.commit()

            response = jsonify({
                "status": "success",
                "message": "Successfully added a new broadcast."
            })

            response = make_response(message)

            return response

        except SQLAlchemyError:
            response = jsonify({
                "status": "fail",
                "message": "An unexpected error occurred."
            })
            response = make_response(response)
            return response

    if request.method == 'GET':
        broadcasts = []

        _broadcasts = Broadcast.query.all()

        for broadcast in _broadcasts:
            broadcasts.append({
                "message": broadcast.message,
                "author": broadcast.get_author(),
                "updated_on": broadcast.updated_on

            })

        response = jsonify(broadcasts)
        return response
