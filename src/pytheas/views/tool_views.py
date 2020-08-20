import urllib.parse

import flask
from flask_login import login_required

from pytheas.services import service, tool_service, user_service, connection_service
from pytheas.utils.view_modifiers import response

blueprint = flask.Blueprint('tool', __name__, template_folder='../templates')


@blueprint.route('/tool/sandbox', methods=['GET'])
@login_required
@response(template_file='home/index.html')
def sandbox():
    return {
        'user': user_service.get_display_name(),
        'projects': user_service.get_projects(),
        'tools': tool_service.get_all_tools(),
    }


@blueprint.route('/tool/build', methods=['GET'])
@login_required
@response(template_file='tool/build.html')
def build():
    return {
        'user': user_service.get_display_name(),
        'projects': user_service.get_projects(),
        'tools': tool_service.get_all_tools(),
        'connections': connection_service.get_connections(user_service.get_current_username()),
    }


@blueprint.route('/tool/connection/check', methods=['POST'])
@login_required
def check_connection():
    data = flask.request.get_json()
    success, message = connection_service.check_connection(user_service.get_current_username(), **data)
    return {
        'status': success,
        'message': message,
    }


@blueprint.route('/tool/connection/create', methods=['POST'])
@login_required
def create_connection():
    data = flask.request.get_json()
    success, message = connection_service.create_connection(user_service.get_current_username(), **data)
    return {
        'status': success,
        'message': message,
    }


@blueprint.route('/tool/explore', methods=['GET'])
@login_required
@response(template_file='home/index.html')
def explore():
    return {
        'user': user_service.get_display_name(),
        'projects': user_service.get_projects(),
        'tools': tool_service.get_all_tools(),
    }


@blueprint.route('/tool/review/<string:connection_name>/<string:connection_id>')
@login_required
@response(template_file='tool/reviewer.html')
def review_connection(connection_name, connection_id):
    doc = connection_service.get_next_record(user_service.get_current_username(), connection_id)
    return {
        'connection_name': connection_name,
        'connection_url': connection_id,
        'previous': None,
        'progress': {},
        'document': doc,
        'history': [],
    }


@blueprint.route('/tool/review/<string:connection_name>/<string:connection_id>/update/<string:name_url>',
                 methods=['POST'])
@login_required
def review_connection_update(connection_name, connection_id, name_url):
    data = flask.request.get_json()
    errors = []
    connection_service.update_tbc(connection_id, urllib.parse.unquote_plus(name_url), **data)
    return {
        'errors': errors,
    }


@blueprint.route('/tool/review/<string:connection_name>/<string:connection_id>/regex/add', methods=['POST'])
@login_required
def review_connection_add_regex(connection_name, connection_id):
    errors = []
    data = flask.request.get_json()
    connection_service.add_regex(connection_id, data['regex'])
    return {
        'errors': errors
    }


@blueprint.route('/tool/review/<string:connection_name>/<string:connection_id>/regex/remove', methods=['POST'])
@login_required
def review_connection_remove_regex(connection_name, connection_id):
    errors = []
    data = flask.request.get_json()
    connection_service.remove_regex(connection_id, data['regex'])
    return {
        'errors': errors
    }


@blueprint.route('/tool/review/<string:connection_name>/<string:connection_id>/previous/<string:name_url>',)
@login_required
@response(template_file='tool/reviewer.html')
def review_connection_prev(connection_name, connection_id, name_url):
    connection_service.mark_done(connection_id, urllib.parse.unquote_plus(name_url))
    doc = connection_service.get_previous_record(user_service.get_current_username(), connection_id)
    return {
        'connection_name': connection_name,
        'connection_url': connection_id,
        'previous': None,
        'progress': {},
        'document': doc,
        'history': [],
    }


@blueprint.route('/tool/review/<string:connection_name>/<string:connection_id>/next/<string:name_url>')
@login_required
@response(template_file='tool/reviewer.html')
def review_connection_next(connection_name, connection_id, name_url):
    connection_service.mark_done(connection_id, urllib.parse.unquote_plus(name_url))
    doc = connection_service.get_next_record(user_service.get_current_username(), connection_id)
    return {
        'connection_name': connection_name,
        'connection_url': connection_id,
        'previous': None,
        'progress': {},
        'document': doc,
        'history': [],
    }
