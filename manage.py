import os

from flask.ext.script import Manager
from apps import app as main_app
from apps.login import User
from apps.manage_utils import _syncdb, _adduser

manager = Manager(main_app)

@manager.command
def syncdb():
    'Create and initialize the db'
    _syncdb()


@manager.command
def adduser(username, password):
    'Add a user'
    _adduser(username, password)

def manage():
    manager.run()

if __name__ == '__main__':
    manage()
