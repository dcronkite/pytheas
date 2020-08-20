import datetime

from pytheas.data.connections import Connection


def get_connections(username):
    return [c for c in Connection.objects(username=username, expiration_date__gt=datetime.datetime.now())]
