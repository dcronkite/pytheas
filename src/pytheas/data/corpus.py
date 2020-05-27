import mongoengine as mongoengine


class Corpus(mongoengine.Document):
    name = mongoengine.StringField()
    path = mongoengine.StringField()
    project = mongoengine.StringField()
