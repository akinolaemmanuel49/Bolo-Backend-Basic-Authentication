import os
import datetime
from dotenv import load_dotenv

BASEDIR_PATH = os.path.abspath(os.path.dirname(__file__))
DOTENV_PATH = os.path.join(os.path.dirname(__file__), ".env")

load_dotenv(dotenv_path=DOTENV_PATH, verbose=True)


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        'SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO')
    JSON_SORT_KEYS = os.environ.get('JSON_SORT_KEYS').lower() == "True".lower()
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=0.5)


# class DevConfig(BaseConfig):


# class ProductionConfig(BaseConfig):


# class TestConfig(BaseConfig):
