import datetime
import enum
import mongoengine as mongoengine


class History(mongoengine.Document):
    username = mongoengine.StringField()
    project_name = mongoengine.StringField()
    subproject_name = mongoengine.StringField()
    annotation_id = mongoengine.ObjectIdField()
    document_name = mongoengine.StringField()
    update_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    how = mongoengine.StringField()
    first_entry = mongoengine.BooleanField(default=False)

    meta = {
        'collection': 'history',
        'db_alias': 'core',
        'indexes': [
            'username',
            'project_name',
            'subproject_name',
            'first_entry',
            '-update_date',
        ]
    }

    @property
    def date_as_string(self):
        return self.update_date.strftime('%Y-%m-%d %H:%M:%S')


class HistoryHow(enum.Enum):
    NEXT = 0
    BY_ANNOT_ID = 1
