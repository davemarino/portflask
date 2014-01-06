# Mixin class for db.Model with some convenience methods
class DBMixin(object):

    def save(self, app):
        "Convenience method to save a model"
        with app.app_context():
            app.extensions['sqlalchemy'].db.session.add(self)
            app.extensions['sqlalchemy'].db.session.commit()
