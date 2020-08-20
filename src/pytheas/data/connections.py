import datetime
import mongoengine

from pytheas.tasks import connection


class Connection(mongoengine.Document):
    connection_name = mongoengine.StringField()
    description = mongoengine.StringField()
    project_name = mongoengine.StringField()
    username = mongoengine.StringField()
    tablename = mongoengine.StringField()
    path = mongoengine.StringField()
    driver = mongoengine.StringField()
    server = mongoengine.StringField()
    database = mongoengine.StringField()
    name_column = mongoengine.StringField()
    text_column = mongoengine.StringField()
    created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    expiration_date = mongoengine.DateTimeField(
        default=lambda: datetime.datetime.now() + datetime.timedelta(days=90)
    )
    ad_hoc_clause = mongoengine.StringField()

    meta = {
        'collection': 'connections',
        'db_alias': 'core',
        'indexes': [
            'connection_name',
            'project_name',
            'username',
        ]
    }

    @property
    def name(self):
        return self.connection_name

    @property
    def connect(self):
        return connection.Connection(
            name=self.connection_name,
            tablename=self.tablename,
            path=self.path,
            driver=self.driver,
            server=self.server,
            database=self.database,
            name_col=self.name_column,
            text_col=self.text_column,
        )
