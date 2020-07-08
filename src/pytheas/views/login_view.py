import flask
from flask import render_template, request, redirect, url_for, current_app
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length

from pytheas.data.users import User
from flask_login import login_user, login_required, logout_user, current_user

from pytheas.services import auth_service

blueprint = flask.Blueprint('login', __name__, template_folder='../templates')


class RegForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=2, max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=2)])
    remember_me = BooleanField('remember_me', default=True)
    skip_ldap = BooleanField('skip_ldap', default=False)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    errors = []
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(username=form.username.data).first()
            if check_user:
                if current_app.config.get('LDAP_SERVER', None) and not form.skip_ldap.data:
                    user_is_valid = auth_service.ldap_authenticate(
                        current_app.config.get('LDAP_SERVER'),
                        current_app.config.get('LDAP_AUTH_USERNAME', ''),
                        form.username.data,
                        form.password.data
                    )
                    if user_is_valid:
                        login_user(check_user, remember=form.remember_me.data)

                        return redirect(url_for('home.index'))
                elif check_password_hash(check_user.hashed_password, form.password.data):
                    login_user(check_user, remember=form.remember_me.data)
                    return redirect(url_for('home.index'))
            else:  # user does not exist
                if current_app.config.get('LDAP_SERVER', None) and not form.skip_ldap.data:
                    user_is_valid = auth_service.ldap_authenticate(
                        current_app.config.get('LDAP_SERVER'),
                        current_app.config.get('LDAP_AUTH_USERNAME', ''),
                        form.username.data,
                        form.password.data
                    )
                    if user_is_valid:  # create new user
                        user = User(
                            username=form.username.data,
                            email=form.username.data,
                        )
                        user.save()
                        login_user(user, remember=form.remember_me.data)
                        return redirect(url_for('home.index'))
                errors.append('Unrecognized username or password.')
        else:
            print(f'Failed to validate: {form.errors}')
    return render_template('login/login.html', form=form, errors=errors)


@blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))
