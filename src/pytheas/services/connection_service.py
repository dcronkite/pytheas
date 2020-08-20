import datetime
import random
import urllib.parse

from pytheas.data.connections import Connection
from pytheas.data.text_by_connections import TextByConnection


def get_connections(username):
    return [{
        'id': c.id,
        'name': c.name,
        'name_url': urllib.parse.quote_plus(c.name),
        'description': c.description,
        'project_name': c.project_name,
        'tablename': f'{c.tablename} ({c.server})' if c.server else None,
        'path': c.path if c.path else None,
        'created_date': c.created_date.strftime('%Y-%m-%d'),
        'expiration_date': c.expiration_date.strftime('%Y-%m-%d'),
    } for c in Connection.objects(username=username, expiration_date__gt=datetime.datetime.now())]


def check_connection(username, **conargs):
    c = Connection(username=username, **conargs)
    success, message = c.connect.test_query()
    return success, message


def create_connection(username, **conargs):
    c = Connection(username=username, **conargs)
    c.save()


def populate_connection(username, connection_id):
    random.randint(0, 100000)
    TextByConnection


def get_next_record(username, connection_id):
    tbc = TextByConnection.objects(
        username=username,
        connection_id=connection_id,
    )
    pass
