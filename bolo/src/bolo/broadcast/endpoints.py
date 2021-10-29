from flask import request, jsonify, make_response

from bolo.broadcast import broadcast

@broadcast.route('/create')
def create_broadcast():
    message = request.json['message']

    message = jsonify(message)

    response = make_response(message)

    return response
