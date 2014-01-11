import unittest
import copy

from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import current_user, logout_user

from apps import create_flask_app, db
from apps.manage_utils import _syncdb, _adduser
from apps.login.models import User

class TestLogin(unittest.TestCase):

    def setUp(self):
        self._app = self._create_app()
        self._app.test_request_context().push()
        self._lm = self._app.extensions["login_manager"]
        _syncdb(self._app)
        user = User('test')
        user.password = 'test'
        self._app.extensions['sqlalchemy'].db.session.add(user)
        self._app.extensions['sqlalchemy'].db.session.commit()

    def tearDown(self):
        User.query.delete()

    def _create_app(self):
        args = {'db': db, 'bcrypt': Bcrypt()}

        class TestingConfig(object):
            TESTING = True
            CSRF_ENABLED = False
            SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

        return create_flask_app(config_object=TestingConfig, **args)

    def test_login_standard_user(self):
        self.assertTrue(self._lm.authenticate_user("test", "test"))

    def test_current_user(self):
        self.assertTrue(current_user.is_anonymous())
        self._lm.authenticate_user("test", "test")
        self.assertEqual(current_user, self._lm.validate_user("test", "test"))

    def test_login_oauth_user(self):
        res = {
            'oauth_token_secret': u'Vh0NZlij1umUoih6S9LSkzWA8D2cTfiAhfEwEHZS8nfrP',
            'user_id': u'486852189',
            'oauth_token': u'486852189-4MLDhCyilpQKPn8T4uOajkbC2ojcB5rnGSIdlgkK',
            'screen_name': u'MarinoDave'
        }

        self.assertTrue(self._lm.authenticate_oauth_user(res, 'twitter'))

        oauth_user = User.query.filter_by(username='486852189').first()

        self.assertIsNotNone(oauth_user)
        self.assertTrue(oauth_user.is_oauth_user)
        self.assertFalse(oauth_user.is_admin)
        self.assertEqual(oauth_user.oauth_service, 'twitter')

        self.assertEqual(oauth_user, current_user)

    def test_login_oauth_user_no_user_id(self):
        res = {
            'oauth_token_secret': u'Vh0NZlij1umUoih6S9LSkzWA8D2cTfiAhfEwEHZS8nfrP',
            'oauth_token': u'486852189-4MLDhCyilpQKPn8T4uOajkbC2ojcB5rnGSIdlgkK',
            'screen_name': u'MarinoDave'
        }

        self.assertFalse(self._lm.authenticate_oauth_user(res, 'twitter'))

    def test_login_oauth_user_already_exists(self):
        res = {
            'oauth_token_secret': u'Vh0NZlij1umUoih6S9LSkzWA8D2cTfiAhfEwEHZS8nfrP',
            'user_id': u'486852189',
            'oauth_token': u'486852189-4MLDhCyilpQKPn8T4uOajkbC2ojcB5rnGSIdlgkK',
            'screen_name': u'MarinoDave'
        }
        # first authentication
        self.assertTrue(self._lm.authenticate_oauth_user(res, 'twitter'))
        logout_user()
        # the second authentication, the method should still
        # return true but it doesn't have to create the user again
        self.assertTrue(self._lm.authenticate_oauth_user(res, 'twitter'))
        oauth_user = User.query.filter_by(username='486852189').first()
        self.assertEqual(current_user, oauth_user)

if __name__ == "__main__":
    unittest.main()
