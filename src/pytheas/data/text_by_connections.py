import mongoengine
import datetime

from pytheas.data.annotation_state import AnnotationState
from pytheas.data.enum_field import EnumField


class TextByConnection(mongoengine.Document):
    connection_id = mongoengine.ObjectIdField()
    username = mongoengine.StringField()
    text_name = mongoengine.StringField()
    text_content = mongoengine.StringField()
    project_name = mongoengine.StringField()
    created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    annotation_state = EnumField(enum_class=AnnotationState)
    annotations = mongoengine.ListField(mongoengine.StringField())
    order = mongoengine.IntField(default=0, min_value=0, max_value=100000)
    metadata = mongoengine.DictField()
    comment = mongoengine.StringField()

    meta = {
        'collection': 'text_by_connections',
        'db_alias': 'core',
        'indexes': [
            'username',
            'project_name',
            '+order',
            'annotation_state',
        ]
    }
