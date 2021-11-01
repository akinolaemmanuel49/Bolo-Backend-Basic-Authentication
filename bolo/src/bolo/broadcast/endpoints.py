from flask import request, jsonify, make_response
from flask.globals import g
from sqlalchemy.exc import SQLAlchemyError

from bolo.broadcast import broadcast
from bolo.models import Broadcast, db
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
                "id": broadcast.id,
                "message": broadcast.message,
                "author": broadcast.get_author().username,
                "updated_on": broadcast.updated_on
            })

        response = jsonify(broadcasts)
        return response


@broadcast.route('/<id>', methods=['PUT'])
@basic_auth.login_required
def edit_broadcast(id):
    message = request.json['message']
    broadcast = Broadcast.query.filter_by(id=id).first()
    if broadcast:
        if broadcast.user_id == basic_auth.current_user().id:
            broadcast.message = message
            try:
                db.session.add(broadcast)
                db.session.commit()

                response = jsonify({
                    "message": "You have successfully editted this broadcast.",
                    "status": "success"
                })
                return response
            except SQLAlchemyError:

                response = jsonify({
                    "message": "An unexpected error occured.",
                    "status": "fail"
                })
                return response
        else:
            response = jsonify({
                "message": "You do not have permission to modify this resource.",
                "status": "fail"
            })
            return response
    response = jsonify({
        "message": "No such entry available in database.",
        "status": "fail"
    })
    return response


@broadcast.route('/<id>', methods=['DELETE'])
@basic_auth.login_required
def delete_broadcast(id):
    broadcast = Broadcast.query.filter_by(id=id).first()
    if broadcast:
        if broadcast.user_id == basic_auth.current_user().id:
            try:
                db.session.delete(broadcast)
                db.session.commit()

                response = jsonify({
                    "message": "You have successfully deleted a broadcast.",
                    "status": "success"
                })

                return response

            except SQLAlchemyError:
                response = jsonify({
                    "message": "An unexpected error occurred.",
                    "status": "fail"
                })

                return response
        else:
            response = jsonify({
                "message": "You do not have permission to modify this resource.",
                "status": "fail"
            })
            return response
    response = jsonify({
        "message": "No such entry available in the database.",
        "status": "fail"
    })
    return response


@broadcast.route('/<id>')
def get_broadcast(id):
    broadcast = Broadcast.query.filter_by(id=id).first()
    if broadcast:
        response = jsonify({
            "id": broadcast.id,
            "message": broadcast.message,
            "author": broadcast.get_author().username,
            "updated_on": broadcast.updated_on
        })
        return response
    response = jsonify({
        "message": "This entry does not exist on the database.",
        "status": "fail"
    })
    return response
