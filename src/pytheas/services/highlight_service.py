from pytheas.data.user_highlights import UserHighlight


def get_highlight(username, project_name):
    return UserHighlight.objects(username=username, project_name=project_name).first()


def get_highlights(username, project_name):
    uh = get_highlight(username, project_name)
    return uh.highlights if uh else list()


def add_highlight(username, project_name, regex):
    uh = get_highlight(username, project_name)
    if not uh:
        uh = UserHighlight(
            username=username,
            project_name=project_name,
        )
    uh.highlights.append(regex)
    uh.save()


def remove_highlight(username, project_name, regex):
    uh = get_highlight(username, project_name)
    if not uh:
        return
    try:
        uh.highlights.remove(regex)
    except ValueError as e:
        return 'Highlight cannot be removed.'
    uh.save()
