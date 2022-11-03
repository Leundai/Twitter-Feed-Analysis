# from api.core import Mixin
from .base import db
from flask_mongoengine import Document
from mongoengine import StringField


class UserProfile(Document):
    """User Profile Collection."""

    name = StringField()

    def __repr__(self):
        return f"""<MentorProfile {self.name}"""
