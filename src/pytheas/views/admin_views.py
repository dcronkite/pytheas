import flask

from pytheas.services import admin_service
from pytheas.utils.view_modifiers import response
from pytheas.viewmodels.admin_viewmodel import AdminTasksViewModel, RegisterUserViewModel, CreateProjectViewModel, \
    AddUserToProjectViewModel, DeleteSubprojectForUser, DeleteSubproject

blueprint = flask.Blueprint('admin', __name__, template_folder='../templates/admin')


@blueprint.route('/admin/tasks', methods=['GET', 'POST'])
@response(template_file='tasks.html')
def admin_tasks():
    vm = AdminTasksViewModel()
    if vm.validate():
        if vm.chosen_task == 'create_user':
            return flask.redirect(flask.url_for('admin.create_user'))
        elif vm.chosen_task == 'create_project':
            return flask.redirect(flask.url_for('admin.create_project'))
        elif vm.chosen_task == 'add_user_to_project':
            return flask.redirect(flask.url_for('admin.add_user_to_project'))
        elif vm.chosen_task == 'delete_subproject_for_user':
            return flask.redirect(flask.url_for('admin.delete_subproject_for_user'))
        elif vm.chosen_task == 'delete_subproject':
            return flask.redirect(flask.url_for('admin.delete_subproject'))
        else:
            admin_service.run_task(vm.chosen_task)
    return vm.to_dict()


@blueprint.route('/admin/tasks/user/create', methods=['GET', 'POST'])
@response(template_file='create_user.html')
def create_user():
    vm = RegisterUserViewModel()
    if vm.validate():
        admin_service.create_user(vm.username, vm.email, vm.password)
    elif vm.back:
        flask.redirect('/admin/tasks')
    return vm.to_dict()


@blueprint.route('/admin/tasks/project/create', methods=['GET', 'POST'])
@response(template_file='create_project.html')
def create_project():
    vm = CreateProjectViewModel()
    if vm.validate():
        admin_service.create_project(vm.project_name, vm.start_date, vm.end_date)
    elif vm.back:
        flask.redirect('/admin/tasks')
    return vm.to_dict()


@blueprint.route('/admin/tasks/project/user', methods=['GET', 'POST'])
@response(template_file='add_user_to_project.html')
def add_user_to_project():
    vm = AddUserToProjectViewModel()
    if vm.validate():
        admin_service.add_users_to_project(vm.usernames, vm.project)
    elif vm.back:
        flask.redirect('/admin/tasks')
    return vm.to_dict()


@blueprint.route('/admin/tasks/subproject/delete/user', methods=['GET', 'POST'])
@response(template_file='delete_subproject_for_user.html')
def delete_subproject_for_user():
    vm = DeleteSubprojectForUser()
    if vm.validate():
        admin_service.delete_subprojects_for_users(vm.project, vm.subprojects, vm.usernames)
    elif vm.back:
        flask.redirect('/admin/tasks')
    return vm.to_dict()


@blueprint.route('/admin/tasks/subproject/delete', methods=['GET', 'POST'])
@response(template_file='delete_subproject.html')
def delete_subproject():
    vm = DeleteSubproject()
    if vm.validate():
        admin_service.delete_subprojects(vm.project, vm.subprojects)
    elif vm.back:
        flask.redirect('/admin/tasks')
    return vm.to_dict()
