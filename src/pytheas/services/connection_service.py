import datetime

from pytheas.data.connections import Connection


def get_connections(username):
    return [c for c in Connection.objects(username=username, expiration_date__gt=datetime.datetime.now())]


def check_connection(username, **conargs):
    c = Connection(username=username, **conargs)
    success, message = c.connect.test_query()
    return success, message
