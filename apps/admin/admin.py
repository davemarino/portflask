import os
from flask.ext.admin import Admin

from flask import Blueprint, send_from_directory
from apps import db
from apps.login.models import User
from apps.portfolio.models import Projects

from views import (MyIndexView, UnaccessibleModelView, UserView)


class AdminApp(object):
    def __init__(self, app=None, app_name=None):
        self.app = None
        if app and app_name:
            self.setup_app(app, app_name)

    def init_app(self, app, app_name):
        self.setup_app(app, app_name)

    def setup_app(self, app, app_name):
        assert self.app == None
        if not self.app:
            self.app = app

        self.__bp = Blueprint('admin_bp', __name__)

        admin = Admin(name=app_name,
                      index_view=MyIndexView(endpoint='adminview'))
        admin.init_app(self.app)

        # adding user view
        admin.add_view(UserView(User, db.session))

        admin.add_view(UnaccessibleModelView(Projects, db.session))

        self.app.register_blueprint(self.__bp)
