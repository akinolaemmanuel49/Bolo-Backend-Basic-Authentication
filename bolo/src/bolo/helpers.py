from flask_httpauth import HTTPBasicAuth

from bolo.models import User

basic_auth = HTTPBasicAuth()

@basic_auth.verify_password
def verify_password(username, password):
    
    user = User.query.filter_by(username=username).first()

    if user and user.check_pwd_hash(password):
        return user