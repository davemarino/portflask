import os

from wtforms import fields as f, widgets as w
from wtforms.validators import Required
from flask import Flask
from flask import abort
from flask.ext.admin import Admin, BaseView, expose, AdminIndexView
from flask.ext.login import current_user, login_required

from wtforms.ext.sqlalchemy.orm import converts

from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.sqla.form import AdminModelConverter
from flask.ext.login import current_user, login_required
from flask.ext.admin.form.upload import FileUploadField

from .forms import validate_url

static_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, os.pardir, 'static')
media_dir = 'media/'


class MyFileUploadField(FileUploadField):

    def __init__(self, *args, **kwargs):
        if 'base_path' not in kwargs or kwargs['base_path'] is None:
            kwargs['base_path'] = static_dir
        if 'relative_path' not in kwargs or kwargs['relative_path'] is None:
            kwargs['relative_path'] = media_dir
        super(MyFileUploadField, self).__init__(*args, **kwargs)

class MyIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        if not current_user.is_admin:
            abort(405)
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
        return current_user.is_authenticated() and current_user.is_admin

class UserView(UnaccessibleModelView):
    column_list = ('username',)
    form_args = dict(
        is_admin=dict(label="Admin", default=False)
    )

class ProjectView(UnaccessibleModelView):
    column_sortable_list = ('name',('project', 'project.name'))
    form_overrides = {'image': MyFileUploadField}
    form_args = dict(
        link=dict(label='Link to the project', validators=[validate_url])
    )
