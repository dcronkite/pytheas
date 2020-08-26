import flask
from flask_login import login_required

import urllib.parse

from pytheas.services import service, user_service, project_service, annotation_service, history_service, abu_service, \
    highlight_service
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
def reviewer(project_url_name):
    project_name = urllib.parse.unquote_plus(project_url_name)
    annot = annotation_service.get_next_annotation(project_name, user_service.get_current_username())
    return _make_reviewer_response(annot, project_name)


def _make_reviewer_response(annot, project_name):
    username = user_service.get_current_username()
    if annot:
        return flask.render_template('review/reviewer.html', **{
            'user': user_service.get_current_user(),
            'project': project_service.get_project_details(project_name),
            'document': annot,
            'history': history_service.get_history_for_link(project_name, username),
            'previous': history_service.get_previous_annotation_id(project_name, username,
                                                                   annot['annotation_id']),
            'progress': abu_service.get_abu_progress(project_name, username)
        })
    else:
        return flask.render_template('review/done.html', **{
            'user': user_service.get_current_user(),
            'project': project_service.get_project_details(project_name),
            'history': history_service.get_history_for_link(project_name, username),
            'previous': None,
        })


@blueprint.route('/project/review/<string:project_url_name>/<string:annotation_id>')
@login_required
def reviewer_specific(project_url_name, annotation_id):
    project_name = urllib.parse.unquote_plus(project_url_name)
    annot = annotation_service.get_annotation_by_id(project_name, annotation_id, user_service.get_current_username())
    return _make_reviewer_response(annot, project_name)


@blueprint.route('/project/review/<string:project_url_name>/<string:annotation_id>/next')
@login_required
def reviewer_next(project_url_name, annotation_id):
    project_name = urllib.parse.unquote_plus(project_url_name)
    username = user_service.get_current_username()
    annotation_service.mark_annotation_completed(project_name, username, annotation_id)
    annot = annotation_service.get_next_annotation(project_name, username)
    return _make_reviewer_response(annot, project_name)


@blueprint.route('/project/review/<string:project_url_name>/<string:annotation_id>/update', methods=['POST'])
@login_required
def update(project_url_name, annotation_id):
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


@blueprint.route('/project/review/<string:project_url_name>/regex/add', methods=['POST'])
@login_required
def add_regex(project_url_name):
    errors = []
    data = flask.request.get_json()
    project_name = urllib.parse.unquote_plus(project_url_name)
    highlight_service.add_highlight(user_service.get_current_username(), project_name, data['regex'])
    return {
        'errors': errors,
    }


@blueprint.route('/project/review/<string:project_url_name>/regex/remove', methods=['POST'])
@login_required
def remove_regex(project_url_name):
    errors = []
    data = flask.request.get_json()
    project_name = urllib.parse.unquote_plus(project_url_name)
    res = highlight_service.remove_highlight(user_service.get_current_username(), project_name, data['regex'])
    if res:
        errors.append(res)
    return {
        'errors': errors,
    }
