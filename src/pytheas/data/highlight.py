import mongoengine


class Highlight(mongoengine.EmbeddedDocument):
    start = mongoengine.IntField()
    end = mongoengine.IntField()
