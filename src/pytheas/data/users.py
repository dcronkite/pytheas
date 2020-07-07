import datetime
import mongoengine
from flask_login import UserMixin


class User(UserMixin, mongoengine.Document):
    username = mongoengine.StringField(unique=True)
    email = mongoengine.StringField(unique=True)
    hashed_password = mongoengine.StringField()
    created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    display_name = mongoengine.StringField(default=None)

    meta = {
        'collection': 'users',
        'db_alias': 'core',
        'indexes': [
            'username',
            'email',
        ]
    }
