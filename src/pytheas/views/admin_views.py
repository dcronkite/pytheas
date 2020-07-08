import flask

from pytheas.services import admin_service
from pytheas.utils.view_modifiers import response
from pytheas.viewmodels.admin_viewmodel import AdminViewModel

blueprint = flask.Blueprint('admin', __name__, template_folder='../../templates/admin')


@blueprint.route('/admin/tasks', methods=['GET', 'POST'])
@response(template_file='tasks.html')
def admin_tasks():
    vm = AdminViewModel()
    if vm.validate():
        admin_service.run_task(vm.chosen_task)
    return vm.to_dict()
