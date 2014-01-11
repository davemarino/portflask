import os
import random

from flask import Blueprint, g, current_app
from flask.ext.login import LoginManager, current_user, login_user, logout_user
from sqlalchemy.exc import InvalidRequestError

from .models import User
from .views import LoginView, LogoutView, OauthAuthView

from oauth import twitter

template_folder = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')), 'templates')

class ExtendedLoginManager(LoginManager):
    def init_app(self, app, add_context_processor=True):
        super(ExtendedLoginManager, self).init_app(app, add_context_processor)
        self._app = app
        self.login_bp = Blueprint('auth', __name__, template_folder=template_folder)

        # define the load user method, applying the @user_loader decorator
        self.load_user = self.user_loader(self.load_user)

        # Login
        self.login_bp.add_url_rule('/login/',
                                view_func=LoginView.as_view('login_view'),
                                methods=['GET', 'POST'])

        # Helper required by Flask-login
        self.login_view = "auth.login_view"

        # Logout
        self.login_bp.add_url_rule('/logout',
                                view_func=LogoutView.as_view('logout_view'))

        twitter_callback = "/complete"
        twitter_handler = OauthAuthView(app, twitter, twitter_callback)
        self.login_bp.add_url_rule('/twitter', view_func=
                twitter_handler.get_authentication_view().as_view('twitter_view'), methods=['POST'])

        self.login_bp.add_url_rule(twitter_callback, view_func=twitter_handler.complete_request)

        app.register_blueprint(self.login_bp)

        if not hasattr(app, 'extensions'):
            app.extensions = {}

        # before_request handlers
        self.g_current_user = app.before_request(self.g_current_user)

        app.extensions['login_manager'] = self

    @staticmethod
    def load_user(userid):
        "Helper function required by Flask-login"

        user = User.query.filter_by(id=userid).first()
        return user or None

    @staticmethod
    def g_current_user():
        "Attach the current_user on the g object"
        g.user = current_user

    def validate_user(self, username, password):
        "Check for valid credentials"

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            return user
        return False

    def authenticate_user(self, username, password):
        "Authenticate user credendials"
        user = self.validate_user(username, password)
        if user:
            login_user(user)
            return True
        return False

    def authenticate_oauth_user(self, res, service):
        user_id = res.get('user_id', None)
        if user_id is None:
            return False
        user = User.query.filter_by(username=user_id).first()
        if user is None:
            user = User(user_id)
            user.password=str(random.getrandbits(64))
            user.is_oauth_user = True
            user.oauth_service = service
            self._app.extensions['sqlalchemy'].db.session.add(user)
            self._app.extensions['sqlalchemy'].db.session.commit()

        login_user(user)

        return True

    def logout_user(self):
        "Logout the current user"
        logout_user()
