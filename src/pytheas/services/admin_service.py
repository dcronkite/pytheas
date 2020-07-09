from pytheas.data.projects import Project
from pytheas.data.users import User
from pytheas.tasks.load_data import load_data


def get_tasks():
    return [
        {'value': 'load_data', 'name': 'Load Data'},
        {'value': 'create_user', 'name': 'Create User'},
        {'value': 'create_project', 'name': 'Create Project'},
        {'value': 'add_user_to_project', 'name': 'Add User to Project'},
    ]


def run_task(chosen_task):
    {
        'load_data': load_data,
    }[chosen_task]()


def add_users_to_project(usernames, project):
    project = Project.objects(project_name=project).first()
    for username in usernames:
        user = User.objects(username=username).first()
        if project.project_name not in user.projects:
            user.projects.append(project.project_name)
            user.save()
        if username not in project.usernames:
            project.usernames.append(username)
            project.save()


def create_project(project_name, start_date, end_date):
    project = Project(project_name=project_name,
                      start_date=start_date,
                      end_date=end_date)
    project.save()


def create_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    user.save()
