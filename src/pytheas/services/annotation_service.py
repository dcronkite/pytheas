from collections import Counter

from pytheas.data.annotation_by_user import AnnotationByUser
from pytheas.data.annotation_state import AnnotationState
from pytheas.data.annotations import Annotation
from pytheas.data.documents import Document


def get_annotation_responses(project_name, username):
    counter = Counter()
    for annot in Annotation.objects(project=project_name, username=username):
        for response in annot.responses:
            counter[response] += 1
    return [{'response': response, 'count': count} for response, count in counter.items()]


def _get_next_abu(project_name, username, state):
    annot = AnnotationByUser.objects(
        project_name=project_name,
        username=username,
        annotation_state=state,
    ).order_by('order').first()
    if annot:
        return annot


def get_next_abu(project_name, username):
    if state := _get_next_abu(project_name, username, AnnotationState.IN_PROGRESS):
        return state
    elif state := _get_next_abu(project_name, username, AnnotationState.READY):
        return state
    return None


def get_next_annotation(project_name, username):
    if not (abu := get_next_abu(project_name, username)):
        return None
    if abu.annotation_id:
        annot = Annotation.objects(id=abu.annotation_id).first()
    else:
        annot = None
    doc = Document.objects(id=abu.document_id).first()
    return {
        'responses': annot.responses if annot else list(),
        'name': doc.document_name,
        'metadata': doc.metadata,
        'text': doc.text,
        'highlights': doc.highlights,
        'offsets': doc.offsets,
        'labels': doc.labels,
    }

