import flask
from flask_login import login_required

import urllib.parse

from pytheas.services import service, user_service, project_service, annotation_service
from pytheas.utils.view_modifiers import response
from pytheas.viewmodels.review_viewmodel import ReviewViewModel

blueprint = flask.Blueprint('review', __name__, template_folder='../templates')


@blueprint.route('/review', methods=['GET'])
@response(template_file='review.html')
def review_get():
    vm = ReviewViewModel()
    return vm.to_dict()


@blueprint.route('/review', methods=['POST'])
@response(template_file='review.html')
def review_post():
    vm = ReviewViewModel()
    if vm.new_regex:
        service.add_regex(vm.new_regex)
    elif vm.remove_regex:
        service.remove_regex(vm.remove_regex)
    vm.reset()
    return vm.to_dict()


@blueprint.route('/project/review/<string:project_url_name>')
@login_required
@response(template_file='review/reviewer.html')
def reviewer(project_url_name):
    project_name = urllib.parse.unquote_plus(project_url_name)
    annot = annotation_service.get_next_annotation(project_name, user_service.get_current_username())
    if annot:
        return {
            'user': user_service.get_current_user(),
            'project': project_service.get_project_details(project_name),
            'document': annot,
        }
    else:
        return {

        }


@blueprint.route('/project/review/<string:project_url_name>/<string:annotation_id>', methods=['POST'])
@login_required
def update_comment(project_url_name, annotation_id):
    data = flask.request.get_json()
    errors = []
    try:
        annotation_service.update_annotation(annotation_id, **data)
    except Exception as e:
        errors.append({
            'header': 'Save Comment Failed',
            'message': str(e)
        })
    return {
        'errors': errors,
    }
