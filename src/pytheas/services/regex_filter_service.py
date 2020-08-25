import re

from pytheas.data.connections import Connection
from pytheas.data.regex_filters import Filter
from pytheas.services import user_service


def add_regex_filter(connection_id, regex, include, exclude, ignore):
    conn = Connection.objects(id=connection_id).first()
    rx_filter = Filter(
        connection_id=connection_id,
        username=user_service.get_current_username(),
        project_name=conn.project_name,
        connection_name=conn.connection_name,
        regex=regex,
        include_flag=include,
        exclude_flag=exclude,
        ignore_flag=ignore,
        active=True,
    )
    rx_filter.save()
    return []


def get_filter(regex_id, connection_id):
    rx_filter = Filter.objects(pk=regex_id).first()
    assert str(rx_filter.connection_id) == connection_id
    return rx_filter


def get_regex_filters(connection_id):
    return [
        {'id': rx.id,
         'regex': rx.regex,
         'include': rx.include_flag,
         'exclude': rx.exclude_flag,
         'ignore': rx.ignore_flag
         }
        for rx in Filter.objects(connection_id=connection_id, active=True)
    ]


def delete_regex_filter(connection_id, regex_id):
    rx_filter = get_filter(regex_id, connection_id)
    rx_filter.active = False
    rx_filter.save()
    return []


def update_regex_filter(connection_id, regex_id, regex, include, exclude, ignore):
    rx_filter = get_filter(regex_id, connection_id)
    rx_filter.regex = regex
    rx_filter.include_flag = include
    rx_filter.exclude_flag = exclude
    rx_filter.ignore_flag = ignore
    rx_filter.save()
    return []


def _build_regex(connection_id, username, *, include_flag=False, exclude_flag=False):
    pattern = '|'.join([rx_filter.regex for rx_filter in Filter.objects(
        username=username,
        connection_id=connection_id,
        active=True,
        include_flag=include_flag,
        exclude_flag=exclude_flag,
    )])
    return re.compile(f'({pattern})', re.I) if pattern else None


def build_inclusion_regex(connection_id, username):
    return _build_regex(connection_id, username, include_flag=True)


def build_exclusion_regex(connection_id, username):
    return _build_regex(connection_id, username, exclude_flag=True)
