from flask import Blueprint

broadcast = Blueprint("broadcast", __name__, url_prefix="/broadcast")

from bolo.broadcast import endpoints