import datetime

import mongoengine


class Annotation(mongoengine.Document):
    username = mongoengine.StringField()
    project = mongoengine.StringField()
    document_id = mongoengine.StringField()
    created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    update_dates = mongoengine.ListField(mongoengine.DateTimeField())
    responses = mongoengine.ListField()

    meta = {
        'collection': 'annotations',
        'db_alias': 'core',
        'indexes': [
            'username',
            'project',
            'document_id',
        ]
    }
