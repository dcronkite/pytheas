import mongoengine
import datetime

from pytheas.data.annotation_state import AnnotationState
from pytheas.data.enum_field import EnumField


class AnnotationByUser(mongoengine.Document):
    username = mongoengine.StringField()
    document_id = mongoengine.ObjectIdField()
    project_name = mongoengine.StringField()
    annotation_id = mongoengine.ObjectIdField()
    created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    annotation_state = EnumField(enum_class=AnnotationState)
    order = mongoengine.IntField(default=0, min_value=0, max_value=100000)

    meta = {
        'collection': 'annotations_by_users',
        'db_alias': 'core',
        'indexes': [
            'username',
            'document_id',
            'project_name',
            '+order',
            'annotation_id',
            'annotation_state',
        ]
    }
