from flask import Blueprint

broadcast = Blueprint("broadcast", __name__)

from bolo.broadcast import endpoints