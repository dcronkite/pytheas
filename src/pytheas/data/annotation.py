import mongoengine


class Annotation(mongoengine.Document):
    label = mongoengine.StringField()
