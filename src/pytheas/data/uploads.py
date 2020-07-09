import datetime
import mongoengine


class Upload(mongoengine.Document):
    name = mongoengine.StringField()
    source_path = mongoengine.StringField()
    project_name = mongoengine.StringField()
    created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    completed_date = mongoengine.DateTimeField()
    completed = mongoengine.BooleanField(default=False)
    document_ids = mongoengine.ListField(mongoengine.ObjectIdField())
    errors = mongoengine.ListField(mongoengine.StringField())

    meta = {
        'collection': 'uploads',
        'db_alias': 'core',
        'indexes': [
            'name',
        ]
    }

    def mark_completed(self):
        self.completed_date = datetime.datetime.now()
        self.completed = True
