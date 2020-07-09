from pytheas.data.projects import Project

import urllib.parse


def get_project_names():
    return [p.project_name for p in Project.objects()]


def get_project_by_name(project_name):
    return Project.objects(project_name=project_name).first()


def get_project_by_url_name(project_name_url):
    return Project.objects(project_name=urllib.parse.unquote_plus(project_name_url))


def get_project_details(project_name):
    project = get_project_by_name(project_name)
    return {
        'name': project.project_name,
        'description': project.description,
        'start_date': project.start_date,
        'end_date': project.end_date,
        'name_url': urllib.parse.quote_plus(project.project_name),
    }
