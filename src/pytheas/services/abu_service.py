"""
Annotations by User Service
"""
from pytheas.data.annotation_by_user import AnnotationByUser
from pytheas.data.annotation_state import AnnotationState


def _get_abu_counts(project_name, username):
    abus = AnnotationByUser.objects(project_name=project_name, username=username).aggregate([
        {'$group': {'_id': '$annotation_state', 'count': {'$sum': 1}}}
    ])
    return abus


def get_abu_details(project_name, username):
    results = []
    for abu in _get_abu_counts(project_name, username):
        results.append({
            'state': AnnotationState(abu['_id']).name,
            'count': abu['count'],
        })
    return results


def get_abu_progress(project_name, username):
    data = {}
    for abu in _get_abu_counts(project_name, username):
        state = AnnotationState(abu['_id'])
        if state in {AnnotationState.READY, AnnotationState.IN_PROGRESS, AnnotationState.DONE}:
            data[state.name] = abu['count']
    total = sum(data.values())
    return {s.lower(): {'percent': round(100 * c / total), 'count': c} for s, c in data.items()}
