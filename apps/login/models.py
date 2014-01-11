from sqlalchemy import types

from flask import current_app
from flask.ext.login import UserMixin

from apps import db
from apps.utils import DBMixin


class Encrypted(types.TypeDecorator):

    impl = types.String

    def process_bind_param(self, value, dialect):
        # encrypt the password before storing in the db
        # if the encrypt extension is installed
        bcrypt = current_app.extensions.get('bcrypt', None)
        if bcrypt:
            return bcrypt.generate_password_hash(value)
        return value


class User(UserMixin, DBMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(Encrypted(120), nullable=False)
    is_admin = db.Column(db.Boolean(name="Admin"), default=False)
    is_oauth_user = db.Column(db.Boolean(name='Logged with Twitter'), default=False)
    oauth_service = db.Column(db.String(50))

    def __init__(self, username=None):
        self.username = unicode(username) or None

    def __repr__(self):
        return '<User %(id)r %(username)r %(is_admin)r %(is_oauth_user)r, %(oauth_service)r>' % {
        'id': self.id,
        'username' : self.username,
        'is_admin' : self.is_admin,
        'is_oauth_user' : self.is_oauth_user,
        'oauth_service' : self.oauth_service
        }

    # Required by admin interface
    def __unicode__(self):
        return self.username

    def check_password(self, plaintext_password):
        "Validate the password against the stored one"
        bcrypt = current_app.extensions.get('bcrypt', None)
        if bcrypt:
            try:
                return bcrypt.check_password_hash(self.password,
                                                    plaintext_password)
            # This happens in case of invalid salt
            except ValueError:
                return False
        else:
            # Bcrypt not installed, check plain text
            return self.password == plaintext_password
