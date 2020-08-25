import mongoengine


class Filter(mongoengine.Document):
    username = mongoengine.StringField()
    project_name = mongoengine.StringField()
    connection_id = mongoengine.ObjectIdField()
    connection_name = mongoengine.StringField()
    regex = mongoengine.StringField()
    include_flag = mongoengine.BooleanField()
    exclude_flag = mongoengine.BooleanField()
    ignore_flag = mongoengine.BooleanField()
    active = mongoengine.BooleanField(default=True)

    meta = {
        'collection': 'regex_filters',
        'db_alias': 'core',
        'indexes': [
            'connection_name',
            'project_name',
            'username',
            'active',
        ]
    }
