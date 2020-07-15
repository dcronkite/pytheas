import mongoengine


class UserHighlight(mongoengine.Document):
    username = mongoengine.StringField()
    project_name = mongoengine.StringField()
    highlights = mongoengine.ListField(mongoengine.StringField())

    meta = {
        'collection': 'user_highlights',
        'db_alias': 'core',
        'indexes': [
            'username',
            'project_name',
        ]
    }
