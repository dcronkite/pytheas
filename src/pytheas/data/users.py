import datetime
import mongoengine
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


class User(UserMixin, mongoengine.Document):
    username = mongoengine.StringField(unique=True)
    email = mongoengine.StringField()
    hashed_password = mongoengine.StringField()
    created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    display_name = mongoengine.StringField(default=None)
    image_url = mongoengine.StringField(default='r_TzuObQYBQ')
    projects = mongoengine.ListField(mongoengine.StringField())

    meta = {
        'collection': 'users',
        'db_alias': 'core',
        'indexes': [
            'username',
            'email',
        ]
    }

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
