import mongoengine
import datetime

from pytheas.data.annotation_state import AnnotationState
from pytheas.data.enum_field import EnumField


class AnnotationByUser(mongoengine.Document):
    username = mongoengine.StringField()
    document_id = mongoengine.StringField()
    project_name = mongoengine.StringField()
    annotation_id = mongoengine.ObjectIdField()
    created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    annotation_state = EnumField(enum_class=AnnotationState)

    meta = {
        'collection': 'annotations_by_users',
        'db_alias': 'core',
        'indexes': [
            'username',
            'document_id',
            'project_name',
            'annotation_id',
            'annotation_state',
        ]
    }