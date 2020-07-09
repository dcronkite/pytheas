import flask
from flask_login import login_required

from pytheas.services import service, user_service
from pytheas.utils.view_modifiers import response
from pytheas.viewmodels.home_viewmodel import HomeViewModel

blueprint = flask.Blueprint('home', __name__, template_folder='../templates')


@blueprint.route('/', methods=['GET'])
@login_required
@response(template_file='home/index.html')
def index():
    return {
        'user': user_service.get_display_name(),
        'projects': user_service.get_projects(),
    }


@blueprint.route('/profile')
@login_required
@response(template_file='home/profile.html')
def profile():
    return {
        'user': user_service.get_current_user(),
    }


@blueprint.route('/config', methods=['POST'])
@response(template_file='home.html')
def config_post():
    vm = HomeViewModel()
    vm.validate()
    if vm.error:
        return vm.to_dict()
    service.save_corpus_path(name=vm.name, corpus_path=vm.corpus_path, project=vm.project)
    resp = flask.redirect('/review')
    return resp
