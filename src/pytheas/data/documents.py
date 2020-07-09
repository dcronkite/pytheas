import datetime
import mongoengine

from pytheas.data.highlight import Highlight


class Document(mongoengine.Document):
    document_name = mongoengine.StringField()
    project_name = mongoengine.StringField()
    username = mongoengine.StringField()
    order = mongoengine.IntField(default=0, min_value=0, max_value=100000)
    text = mongoengine.StringField()
    highlights = mongoengine.ListField(mongoengine.StringField())
    created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    expiration_date = mongoengine.DateTimeField(
        default=lambda: datetime.datetime.now() + datetime.timedelta(days=90)
    )
    offsets = mongoengine.EmbeddedDocumentListField(Highlight)
    metadata = mongoengine.DictField()
    labels = mongoengine.ListField(mongoengine.StringField())

    meta = {
        'collection': 'documents',
        'db_alias': 'core',
        'indexes': [
            'document_name',
            'project_name',
            'username',
            '+order',
        ]
    }

    @property
    def name(self):
        return self.document_name
