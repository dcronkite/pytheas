from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import InputRequired, Length

from pytheas.services import admin_service, user_service, project_service
from pytheas.viewmodels.viewmodelbase import ViewModelBase


class AdminTasksViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.tasks = admin_service.get_tasks()
        self.chosen_task = self.request_dict.chosen_task

    def validate(self):
        return bool(self.chosen_task)


class CreateUserForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=2, max=30)])
    email = EmailField('username', validators=[InputRequired(), Length(min=2, max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=2)])


class RegisterUserViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.form = CreateUserForm()
        self.back = self.request_dict.back
        self.errors = []

    def validate(self):
        if not self.form.validate():
            return False
        if self.username in user_service.get_usernames():
            self.errors.append('Username already exists')
            return False
        return True

    @property
    def username(self):
        return self.form.username.data

    @property
    def email(self):
        return self.form.email.data

    @property
    def password(self):
        return self.form.password.data


class CreateProjectForm(FlaskForm):
    project_name = StringField('project_name', validators=[InputRequired()])
    start_date = DateField('start_date', validators=[InputRequired()])
    end_date = DateField('end_date', validators=[InputRequired()])


class CreateProjectViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.form = CreateProjectForm()
        self.back = self.request_dict.back
        self.errors = []

    def validate(self):
        return self.form.validate()

    @property
    def project_name(self):
        return self.form.project_name.data

    @property
    def start_date(self):
        return self.form.start_date.data

    @property
    def end_date(self):
        return self.form.end_date.data


class AddUserToProjectForm(FlaskForm):
    project_name = SelectField('project_name', validators=[InputRequired()])
    usernames = SelectMultipleField('usernames', validators=[InputRequired()])


class AddUserToProjectViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.form = AddUserToProjectForm()
        self.form.project_name.choices = [('', '')] + [(name, name) for i, name in
                                                       enumerate(project_service.get_project_names())]
        self.form.usernames.choices = [('', '')] + [(name, name) for i, name in enumerate(user_service.get_usernames())]
        self.back = self.request_dict.back
        self.errors = []

    @property
    def project(self):
        return self.form.project_name.data

    @property
    def usernames(self):
        return self.form.usernames.data

    def validate(self):
        if not self.form.validate():
            return False
        if '' in self.usernames:
            return False
        if not self.project:
            return False
        return True


class DeleteSubprojectForUserForm(FlaskForm):
    project_name = SelectField('project_name', validators=[InputRequired()])
    usernames = SelectMultipleField('usernames', validators=[InputRequired()])
    subprojects = SelectMultipleField('subproject', validators=[InputRequired()])


class DeleteSubprojectForUser(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.form = DeleteSubprojectForUserForm()
        projects = project_service.get_project_names()
        self.form.project_name.choices = [('', '')] + [(name, name) for i, name in
                                                       enumerate(projects)]
        self.form.usernames.choices = [('', '')] + [(name, name) for i, name in enumerate(user_service.get_usernames())]
        self.form.subprojects.choices = [('', '')] + [
            (name, name) for i, name in enumerate(sp['name'] for p in projects for sp in project_service.get_subprojects(p))
        ]
        self.back = self.request_dict.back
        self.errors = []

    @property
    def project(self):
        return self.form.project_name.data

    @property
    def usernames(self):
        return self.form.usernames.data

    @property
    def subprojects(self):
        return self.form.subproject.data

    def validate(self):
        if not self.form.validate():
            return False
        if '' in self.usernames:
            return False
        if not self.project:
            return False
        if not self.subprojects:
            return False
        return True


class DeleteSubprojectForm(FlaskForm):
    project_name = SelectField('project_name', validators=[InputRequired()])
    subprojects = SelectMultipleField('subproject', validators=[InputRequired()])


class DeleteSubproject(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.form = DeleteSubprojectForm()
        projects = project_service.get_project_names()
        self.form.project_name.choices = [('', '')] + [(name, name) for i, name in
                                                       enumerate(projects)]
        self.form.subprojects.choices = [('', '')] + [
            (name, name) for i, name in enumerate(sp['name'] for p in projects for sp in project_service.get_subprojects(p))
        ]
        self.back = self.request_dict.back
        self.errors = []

    @property
    def project(self):
        return self.form.project_name.data

    @property
    def subprojects(self):
        return self.form.subprojects.data

    def validate(self):
        if not self.form.validate():
            return False
        if not self.project:
            return False
        if not self.subprojects:
            return False
        return True
