import urllib.parse

from pytheas.data.users import User
from flask_login import current_user


def get_usernames():
    return [u.username for u in User.objects()]


def get_display_name():
    return {
        'display_name': current_user.display_name or current_user.username,
        'display_image': current_user.image_url,
    }


def get_current_user():
    return {
        'display_name': current_user.display_name or current_user.username,
        'display_image': current_user.image_url,
        'name': current_user.display_name,
        'email': current_user.email,
        'username': current_user.username,
        'created_date': current_user.created_date.strftime('%B %Y'),
    }


def get_current_user_id():
    return current_user.id


def update_display_name(new_display_name):
    # TODO: validation of name
    current_user.display_name = new_display_name
    current_user.save()


def get_projects():
    return [
        {'name': project, 'url_name': urllib.parse.quote(project)}
        for project in current_user.projects
    ]
