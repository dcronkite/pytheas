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
@response(template_file='review/reviewer.html')
def review_connection(connection_name, connection_id):
    connection_name = urllib.parse.unquote_plus(connection_name)
    print(connection_id)
    return {}
