from pytheas.data.annotation_by_user import AnnotationByUser
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
    first_entry = not bool(History.objects(
        username=username,
        document_name=document_name,
        project_name=project_name,
        annotation_id=annotation_id,
    ).first())
    History(
        username=username,
        document_name=document_name,
        project_name=project_name,
        annotation_id=annotation_id,
        first_entry=first_entry,
        how=how.name,
    ).save()


def get_previous_annotation_id(project_name, username, curr_annotation_id):
    curr = History.objects(
        project_name=project_name,
        username=username,
        annotation_id=curr_annotation_id,
        first_entry=True,
    ).first()
    h = History.objects(
        project_name=project_name,
        username=username,
        update_date__lt=curr.update_date,
        first_entry=True,
    ).order_by('-update_date').first()
    return h.annotation_id if h else None
