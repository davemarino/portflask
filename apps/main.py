import os
from flask import (Flask, render_template, Blueprint, current_app, request,
                   abort)
from flask_debugtoolbar import DebugToolbarExtension

template_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'templates')
static_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'static')

# Applying the Application Factory pattern
# http://bit.ly/Pjc5N3, slide 53

bp = Blueprint('common', __name__, template_folder=template_dir)


# defining routes
@bp.route('/')
def index():
    # return "Fist app"
    return render_template('index.html')


def create_flask_app(config_file=None, config_object=None, **kwargs):
    """Create and configure the Flask application. Accepted parameters are:
        :param db: A Flask-SQLAlchemy instance
        :param bcrypt: (optional) -> A Flask-Bcrypt instance
    """
    app = Flask(__name__, static_folder=static_dir)

    # Setting default values
    app.config['SECRET_KEY'] = 'test'
    app.debug = True

    # Creating instance path
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    if 'db' in kwargs:
        db_path = 'sqlite:///%s/%s' % (app.instance_path, 'test.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = db_path

    # first override configurations from object if any
    if config_object:
        app.config.from_object(config_object)

    # then override configurations from file if any
    if config_file:
        app.config.from_pyfile(config_file)

    # then override configuration from envvar
    if 'PORTFOLIO_SETTINGS' in os.environ:
        app.config.from_envvar('PORTFOLIO_SETTINGS')

    if app.debug and not app.config.get('TESTING', None):
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        app.config['DEBUG_TB_PROFILER_ENABLED'] = True
        app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
        DebugToolbarExtension(app)

    # Ensure we have an extensions registry on the app
    if not hasattr(app, 'extensions'):
        app.extensions = {}

    # registering apps / exensions
    if 'db' in kwargs:
        kwargs['db'].init_app(app)

    if 'bcrypt' in kwargs:
        kwargs['bcrypt'].init_app(app)
        # Store the bcrypt object in the extensions registry
        app.extensions['bcrypt'] = kwargs['bcrypt']

    app.config['TWITTER'] = dict(
        consumer_key='Y3VbmvbZnNSIWNkvhopuUA',
        consumer_secret='JtiVYgJRGCNWBRZIOaF6HSoDBtsZAkXmQEAYgNgZOU',
        base_url='https://api.twitter.com/',
        request_token_url='https://api.twitter.com/oauth/request_token',
        access_token_url='https://api.twitter.com/oauth/access_token',
        authorize_url='https://api.twitter.com/oauth/authorize',
    )

    from .login import LoginManager
    from .login.oauth import oauth

    login_manager = LoginManager()
    login_manager.init_app(app)
    oauth.init_app(app)

    from .admin import AdminApp

    AdminApp(app, 'admin')

    app.register_blueprint(bp)

    # register jinja filters
    jinja_environment = app.create_jinja_environment()
    app.create_jinja_environment = lambda *args: jinja_environment

    return app
