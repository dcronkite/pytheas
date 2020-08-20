import urllib.parse

import flask
from flask_login import login_required

from pytheas.services import service, abu_service, project_service, user_service, annotation_service, tool_service
from pytheas.utils.view_modifiers import response

blueprint = flask.Blueprint('project', __name__, template_folder='../templates')


@blueprint.route('/project/<string:project_url_name>')
@login_required
@response(template_file='project/project.html')
def project_home(project_url_name):
    project_name = urllib.parse.unquote_plus(project_url_name)
    return {
        'user': user_service.get_current_user(),
        'project_details': project_service.get_project_details(project_name),
        'review_details': abu_service.get_abu_details(
            project_name,
            user_service.get_current_username(),
        ),
        'tools': tool_service.get_all_tools(),
        'annotation_summary': annotation_service.get_annotation_responses(
            project_name, user_service.get_current_username(),
        )
    }
