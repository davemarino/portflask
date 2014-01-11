from flask_oauthlib.client import OAuth

oauth = OAuth()

twitter = oauth.remote_app(
            'twitter',
            app_key="TWITTER"
        )
