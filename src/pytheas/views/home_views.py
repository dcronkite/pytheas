import flask

from pytheas.services import service
from pytheas.utils.view_modifiers import response
from pytheas.viewmodels.home_viewmodel import HomeViewModel

blueprint = flask.Blueprint('home', __name__, template_folder='../../templates')


@blueprint.route('/', methods=['GET'])
@blueprint.route('/config', methods=['GET'])
@response(template_file='home.html')
def index():
    vm = HomeViewModel()
    return vm.to_dict()


@blueprint.route('/', methods=['POST'])
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
