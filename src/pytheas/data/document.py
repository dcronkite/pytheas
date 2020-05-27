import mongoengine

from pytheas.data.annotation import Annotation
from pytheas.data.corpus import Corpus


class Document(mongoengine.Document):
    name = mongoengine.StringField(unique=True)
    length = mongoengine.IntField()
    annotations = mongoengine.ListField(mongoengine.ReferenceField(Annotation))
    corpora = mongoengine.ListField(mongoengine.ReferenceField(Corpus))

    meta = {
        'collection': 'documents',
        'db_alias': 'core',
        'indexes': [
            'name',
            'length',
        ]
    }
