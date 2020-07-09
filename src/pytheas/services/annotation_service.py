from collections import Counter

from pytheas.data.annotations import Annotation


def get_annotation_responses(project_name, username):
    counter = Counter()
    for annot in Annotation.objects(project=project_name, username=username):
        for response in annot.responses:
            counter[response] += 1
    return [{'response': response, 'count': count} for response, count in counter.items()]
