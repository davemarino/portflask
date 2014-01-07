from sqlalchemy import types
from sqlalchemy.orm import validates

from flask import current_app

from apps import db
from apps.utils import DBMixin

class Projects(DBMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    link = db.Column(db.String)
    image = db.Column(db.String(400))

    def __init__(self, name=None, description=None):
        self.name = unicode(name) or None
        self.description = unicode(description) or None

    def __repr__(self):
        return '<Project %r>' % self.name

    # Required by admin interface
    def __unicode__(self):
        return self.name
