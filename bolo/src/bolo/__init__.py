from flask import Flask
from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from bolo.config import BaseConfig
from bolo.broadcast import broadcast

# Constants
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()


def create_app(config_class=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize middleware/extensions
    initialize_extensions(app)
    # Register blueprints
    app.register_blueprint(broadcast)
    # register_blueprints(app)

    return app


def initialize_extensions(app):
    from bolo.models import db
    db.init_app(app)

    migrate.init_app(app, db)
    cors.init_app(app)


def register_blueprints(app):
    from bolo.broadcast import broadcast
    app.register_blueprint(broadcast)


app = create_app()
