from pytheas.data.histories import History, HistoryHow


def get_history(project_name, username, n=20) -> History:
    return History.objects(
        project_name=project_name,
        username=username
    ).order_by('-update_date')[:n]


def get_history_for_link(project_name, username, n=20):
    return [
        {
            'document_name': h.document_name,
            'annotation_id': h.annotation_id,
            'update_date': h.date_as_string,
        } for h in get_history(project_name, username, n=n)
    ]


def write_history(annotation_id, project_name, username, document_name, how: HistoryHow):
    History(
        username=username,
        document_name=document_name,
        project_name=project_name,
        annotation_id=annotation_id,
        how=how.name,
    ).save()
