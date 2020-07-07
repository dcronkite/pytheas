import datetime
import mongoengine

from pytheas.data.highlight import Highlight


class Document(mongoengine.Document):
    document_id = mongoengine.StringField()
    project_name = mongoengine.StringField()
    username = mongoengine.StringField()
    order = mongoengine.IntField(default=0, min_value=0, max_value=100000)
    text = mongoengine.StringField(unique=True)
    highlights = mongoengine.ListField(mongoengine.StringField())
    created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    expiration_date = mongoengine.DateTimeField(
        default=lambda: datetime.datetime.now() + datetime.timedelta(days=30)
    )
    offsets = mongoengine.EmbeddedDocumentListField(Highlight)
    metadata = mongoengine.DictField()

    meta = {
        'collection': 'documents',
        'db_alias': 'core',
        'indexes': [
            'document_id',
            'project_name',
            'username',
            '+order',
        ]
    }
