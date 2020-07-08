from pytheas.data.projects import Project


def get_project_names():
    return [p.project_name for p in Project.objects()]
