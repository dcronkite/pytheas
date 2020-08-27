import datetime

import mongoengine


class Project(mongoengine.Document):
    project_name = mongoengine.StringField(unique=True)
    description = mongoengine.StringField()
    created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    start_date = mongoengine.DateTimeField()
    end_date = mongoengine.DateTimeField()
    usernames = mongoengine.ListField(mongoengine.StringField())
    subprojects = mongoengine.ListField(mongoengine.StringField())

    meta = {
        'collection': 'projects',
        'db_alias': 'core',
        'indexes': [
            'project_name',
        ]
    }

    @property
    def name(self):
        return self.project_name

    @property
    def is_active(self):
        return self.end_date <= datetime.datetime.now() <= self.start_date
