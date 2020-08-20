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


def populate_connection(connection):
    for i, (name, text, metadata) in enumerate(connection.connect.iterate(

    )):
        random.randint(0, 100000)
        TextByConnection


def _get_connection(connection_id):
    return Connection.objects(id=connection_id).first()


def get_record(iterator, connection_id, *, inclusion_regex=None, exclusion_regex=None):
    c = _get_connection(connection_id)
    m = None
    for tbc in iterator:
        if exclusion_regex and exclusion_regex.search(tbc.text_content):
            if tbc.annotation_state in [AnnotationState.IN_PROGRESS, AnnotationState.READY]:
                tbc.annotation_state = AnnotationState.SKIPPED
                tbc.save()
        elif not inclusion_regex or (m := inclusion_regex.search(tbc.text_content)):
            tbc.annotation_state = AnnotationState.IN_PROGRESS
            tbc.save()
            return {
                'name': tbc.text_name,
                'name_url': urllib.parse.quote_plus(tbc.text_name),
                'responses': c.options,
                'labels': tbc.annotations,
                'comment': tbc.comment,
                'preview': [tbc.text_content[max(0, m.start() - 30): m.end() + 30]] if m else [],
                'sentences': annotation_service.get_highlighted_sentences(tbc.text_content, highlights=c.highlights),
                'highlights': c.highlights,
            }


def get_previous_record(username, connection_id, inclusion_regex=None, exclusion_regex=None):
    return get_record(
        TextByConnection.objects(
            username=username,
            connection_id=connection_id,
            annotation_state__in=[AnnotationState.SKIPPED, AnnotationState.DONE],
        ).order_by('-order'),
        connection_id,
        inclusion_regex=inclusion_regex,
        exclusion_regex=exclusion_regex,
    )


def get_next_record(username, connection_id, inclusion_regex=None, exclusion_regex=None):
    return get_record(
        TextByConnection.objects(
            username=username,
            connection_id=connection_id,
            annotation_state__in=[AnnotationState.IN_PROGRESS, AnnotationState.READY],
        ).order_by('order'),
        connection_id,
        inclusion_regex=inclusion_regex,
        exclusion_regex=exclusion_regex,
    )


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

