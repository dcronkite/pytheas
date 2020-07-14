import re
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


def get_next_annotation(project_name, username, highlights=None):
    if not (abu := get_next_abu(project_name, username)):
        return None
    doc = Document.objects(id=abu.document_id).first()
    if abu.annotation_id:
        annot = Annotation.objects(id=abu.annotation_id).first()
    else:
        annot = Annotation(
            username=username,
            project=project_name,
            document_id=doc.id,
        )
        annot.save()
        abu.annotation_id = annot.id
        abu.save()
    print(annot.id, annot.comment)
    preview = []
    sentences = []
    highlights = doc.highlights + highlights if highlights else []
    pat = None if not highlights else re.compile(rf"\b({'|'.join(rx for rx in highlights if rx)})\w*\b", re.IGNORECASE)
    start = 0
    for line in doc.text.split('\n'):
        sent_start = start
        sent_end = sent_start + len(line)
        emphasize = False
        for offset in doc.offsets:
            if sent_start <= offset.start < sent_end or sent_start <= offset.end < sent_end:
                emphasize = True
                break
        sentence = []
        if pat:
            for m in pat.finditer(line):
                sentence.append({
                    'text': doc.text[sent_start:m.start() + sent_start],
                    'emphasize': emphasize,
                    'highlight': False
                })
                sentence.append({
                    'text': doc.text[m.start() + sent_start:m.end() + sent_start],
                    'emphasize': emphasize,
                    'highlight': True
                })
                sent_start = m.end() + sent_start
        sentence.append({
            'text': doc.text[sent_start:sent_end],
            'emphasize': emphasize,
            'highlight': False,
        })
        sentences.append(sentence)
        start = sent_end
    for offset in sorted(doc.offsets):
        preview.append(doc.text[offset.start:offset.end])
    return {
        'annotation_id': annot.id,
        'comment': annot.comment,
        'responses': annot.responses,
        'name': doc.document_name,
        'metadata': doc.metadata,
        'text': doc.text,
        'highlights': doc.highlights,
        'offsets': doc.offsets,
        'labels': doc.labels,
        'sentences': sentences,
        'preview': preview,
    }


def get_annotation(annot_id):
    return Annotation.objects(id=annot_id).first()


def update_annotation_comment(annot_id, comment):
    update_annotation(annot_id, comment=comment)


def update_annotation_response(annot_id, *responses):
    update_annotation(annot_id, responses=responses)


def update_annotation(annot_id, **fields):
    annot = get_annotation(annot_id)
    for key, value in fields.items():
        annot[key] = value
    print(annot.comment)
    annot.save()
    print(annot.comment)
