import flask
from flask import session

from pytheas import service
from pytheas.utils.view_modifiers import response
from pytheas.viewmodels.review_viewmodel import ReviewViewModel

blueprint = flask.Blueprint('review', __name__, template_folder='../../templates')


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
        vm.reset()
        return vm.to_dict()
    elif vm.remove_regex:
        service.remove_regex(vm.remove_regex)
        vm.reset()
        return vm.to_dict()
    return vm.to_dict()
