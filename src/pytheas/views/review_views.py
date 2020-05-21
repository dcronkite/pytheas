import flask

from pytheas.utils.view_modifiers import response
from pytheas.viewmodels.review_viewmodel import ReviewViewModel

blueprint = flask.Blueprint('review', __name__, template_folder='../../templates')


@blueprint.route('/review', methods=['GET'])
@response(template_file='review.html')
def index():
    vm = ReviewViewModel()
    return vm.to_dict()
