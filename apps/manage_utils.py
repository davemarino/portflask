import os

from apps import app as main_app
from apps.login import User

def _syncdb(app=None):

    # using main_app if an app is not passed
    app = app or main_app

    app.logger.info('Syncing db...')

    driver = app.config['SQLALCHEMY_DATABASE_URI']

    # Handling db path creation
    if driver.startswith('sqlite'):
        app.logger.info('[*] sqlite driver found')
        if not ('memory' in driver):
            path = driver.replace('sqlite:///', '')
            path = os.path.split(path)[0]
            if not os.path.exists(path):
                os.makedirs(path)
        else:
            app.logger.info('[*] in-memory db,nothing to do')
            pass

    # create tables
    with app.app_context():
        app.logger.info('[*] creating tables')
        app.extensions['sqlalchemy'].db.create_all()

def _adduser(username, password, app=None):
    # using main_app if an app is not passed
    app = app or main_app

    # put the app in debug for logging purpose
    app.debug = True

    admin = User(username)
    admin.password = password
    admin.is_admin = True
    try:
        admin.save(app)
        if not app.config['TESTING']:
            app.logger.info('User %s created' % username)
    except:
        if not app.config['TESTING']:
            app.logger.info('Unable to create the user %s' % username)

    # Deactivate the debug mode
    app.debug = False
