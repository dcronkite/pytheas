import datetime

import mongoengine


class Annotation(mongoengine.Document):
    username = mongoengine.StringField()
    project = mongoengine.StringField()
    subproject = mongoengine.StringField()
    document_id = mongoengine.ObjectIdField()
    created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    update_dates = mongoengine.ListField(mongoengine.DateTimeField())
    responses = mongoengine.ListField()
    comment = mongoengine.StringField()

    meta = {
        'collection': 'annotations',
        'db_alias': 'core',
        'indexes': [
            'username',
            'project',
            'subproject',
            'document_id',
        ]
    }

    def to_json(self):
        return {
            'username': self.username,
            'project': self.project,
            'subproject': self.subproject,
            'responses': self.responses,
        }
