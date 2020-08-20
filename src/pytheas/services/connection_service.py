import datetime
import random
import urllib.parse

from pytheas.data.annotation_state import AnnotationState
from pytheas.data.connections import Connection
from pytheas.data.text_by_connections import TextByConnection
from pytheas.services import annotation_service


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
    return True, 'Successful, refresh to see connection'


def populate_connection(connection: Connection, username, *,
                        max_instances=100000, include_regex=None, exclude_regex=None):
    for i, (name, text, metadata) in enumerate(connection.connect.iterate(
            include_regex=include_regex, exclude_regex=exclude_regex
    )):
        if i >= max_instances:
            return
        tbc = TextByConnection(
            connection_id=connection.id,
            username=username,
            text_name=name,
            text_content=text,
            project_name=connection.project_name,
            annotation_state=AnnotationState.READY,
            order=random.randint(0, 100000),
            metadata=metadata,
        )
        tbc.save()


def _get_connection(connection_id):
    return Connection.objects(id=connection_id).first()


def _get_record(tbc_dict, order_by, c, *, inclusion_regex=None, exclusion_regex=None):
    m = None
    i = None
    for i, tbc in enumerate(
            TextByConnection.objects(**tbc_dict).order_by(order_by)
    ):
        if exclusion_regex and exclusion_regex.search(tbc.text_content):
            if tbc.annotation_state in [AnnotationState.IN_PROGRESS.value, AnnotationState.READY.value]:
                tbc.annotation_state = AnnotationState.SKIPPED
                tbc.save()
        elif not inclusion_regex or (m := inclusion_regex.search(tbc.text_content)):
            tbc.annotation_state = AnnotationState.IN_PROGRESS.value
            tbc.save()
            return i, {
                'name': tbc.text_name,
                'name_url': urllib.parse.quote_plus(tbc.text_name),
                'responses': c.options,
                'labels': tbc.annotations,
                'comment': tbc.comment,
                'preview': [tbc.text_content[max(0, m.start() - 30): m.end() + 30]] if m else [],
                'sentences': annotation_service.get_highlighted_sentences(tbc.text_content, highlights=c.highlights),
                'highlights': c.highlights,
                'metadata': tbc.metadata,
            }
    return i, None


def get_record(tbc_dict, order_by, connection_id, username, *, inclusion_regex=None, exclusion_regex=None):
    """

    :param tbc_dict:
    :param order_by:
    :param connection_id:
    :param username:
    :param inclusion_regex:
    :param exclusion_regex:
    :return: is_done, record
    """
    c = _get_connection(connection_id)
    i, tbc = _get_record(tbc_dict, order_by, c, inclusion_regex=inclusion_regex, exclusion_regex=exclusion_regex)
    if tbc:
        return tbc
    if i is None:  # nothing loaded
        populate_connection(c, username, include_regex=inclusion_regex, exclude_regex=exclusion_regex)
        i, tbc = _get_record(tbc_dict, order_by, c, inclusion_regex=inclusion_regex, exclusion_regex=exclusion_regex)
        if tbc:
            return tbc
    return None  # TODO: handle completed review


def get_previous_record(username, connection_id, inclusion_regex=None, exclusion_regex=None):
    return get_record(
        {
            'username': username,
            'connection_id': connection_id,
            'annotation_state__in': [AnnotationState.SKIPPED, AnnotationState.DONE]
        },
        '-order',
        connection_id,
        username,
        inclusion_regex=inclusion_regex,
        exclusion_regex=exclusion_regex,
    )


def get_next_record(username, connection_id, inclusion_regex=None, exclusion_regex=None):
    return get_record(
        {
            'username': username,
            'connection_id': connection_id,
            'annotation_state__in': [AnnotationState.IN_PROGRESS, AnnotationState.READY],
        },
        'order',
        connection_id,
        username,
        inclusion_regex=inclusion_regex,
        exclusion_regex=exclusion_regex,
    )


def mark_done(connection_id, text_name):
    tbc = TextByConnection.objects(connection_id=connection_id, text_name=text_name).first()
    tbc.annotation_state = AnnotationState.DONE
    tbc.save()


def update_tbc(connection_id, text_name, **fields):
    tbc = TextByConnection.objects(connection_id=connection_id, text_name=text_name).first()
    for key, value in fields.items():
        tbc[key] = value
    tbc.save()


def add_regex(connection_id, regex):
    c = _get_connection(connection_id)
    c.highlights.append(regex)
    c.save()


def remove_regex(connection_id, regex):
    c = _get_connection(connection_id)
    try:
        c.highlights.remove(regex)
    except ValueError as e:
        pass
    c.save()
