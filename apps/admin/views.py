from wtforms import fields as f, widgets as w
from flask import Flask
from flask.ext.admin import Admin, BaseView, expose, AdminIndexView
from flask.ext.login import current_user, login_required

from wtforms.ext.sqlalchemy.orm import converts

from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.admin.contrib.sqlamodel.form import AdminModelConverter
from flask.ext.login import current_user, login_required

class MyIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        return self.render('admin/index.html')


# Adding coverter for the new Encrypted field
@converts('Encrypted')
def conv_Encrypted(self, field_args, **extra):
    field_args['widget'] = w.PasswordInput()
    self._string_common(field_args=field_args, **extra)
    return f.TextField(**field_args)

AdminModelConverter.conv_Encrypted = conv_Encrypted


class UnaccessibleModelView(ModelView):
    # Receive a 403 FORBIDDEN if not authenticated
    def is_accessible(self):
        return current_user.is_authenticated()

class UserView(UnaccessibleModelView):
	list_columns = ('username',)
