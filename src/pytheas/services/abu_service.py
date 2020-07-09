"""
Annotations by User Service
"""
from pytheas.data.annotation_by_user import AnnotationByUser
from pytheas.data.annotation_state import AnnotationState


def get_abu_details(project_name, username):
    abus = AnnotationByUser.objects(project_name=project_name, username=username).aggregate([
        {'$group': {'_id': '$annotation_state', 'count': {'$sum': 1}}}
    ])
    results = []
    for abu in abus:
        results.append({
            'state': AnnotationState(abu['_id']).name,
            'count': abu['count'],
        })
    return results
