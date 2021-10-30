from flask import Blueprint

auth = Blueprint("auth", __name__, url_prefix="/user")

from bolo.auth import endpoints