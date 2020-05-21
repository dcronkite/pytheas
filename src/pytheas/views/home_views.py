import flask

from pytheas.utils.view_modifiers import response

blueprint = flask.Blueprint('home', __name__, template_folder='../../templates')


@blueprint.route('/', methods=['GET'])
@response(template_file='home.html')
def index():
    return {}
