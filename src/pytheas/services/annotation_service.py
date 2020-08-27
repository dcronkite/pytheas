import datetime
import re
from collections import Counter

from pytheas.data.annotation_by_user import AnnotationByUser
from pytheas.data.annotation_state import AnnotationState
from pytheas.data.annotations import Annotation
from pytheas.data.documents import Document
from pytheas.data.histories import HistoryHow
from pytheas.services import highlight_service
from pytheas.services.history_service import write_history


def get_annotation_responses(project_name, username, **kwargs):
    kwargs = {x: y for x, y in kwargs.items() if y}
    counter = Counter()
    for annot in Annotation.objects(project=project_name, username=username, **kwargs):
        for response in annot.responses:
            counter[response] += 1
    return [{'response': response, 'count': count} for response, count in counter.items()]


def _get_next_abu(project_name, username, state, subproject_name=None):
    if subproject_name:
        annot = AnnotationByUser.objects(
            project_name=project_name,
            username=username,
            annotation_state=state,
            subproject_name=subproject_name,
        ).order_by('order').first()
    else:
        annot = AnnotationByUser.objects(
            project_name=project_name,
            username=username,
            annotation_state=state,
        ).order_by('order').first()
    if annot:
        return annot


def get_next_abu(project_name, username, subproject_name):
    if state := _get_next_abu(project_name, username, AnnotationState.IN_PROGRESS, subproject_name):
        return state
    elif state := _get_next_abu(project_name, username, AnnotationState.READY, subproject_name):
        return state
    return None


def _get_or_create_annotation(abu: AnnotationByUser, set_state: AnnotationState = None) -> (Annotation, Document):
    doc = Document.objects(id=abu.document_id).first()
    if abu.annotation_id:
        annot = Annotation.objects(id=abu.annotation_id).first()
    else:
        annot = Annotation(
            username=abu.username,
            project=abu.project_name,
            document_id=doc.id,
        )
        annot.save()
        abu.annotation_id = annot.id
    if set_state:
        abu.annotation_state = set_state
    abu.save()
    return annot, doc


def _get_abu_response(annot: Annotation, doc: Document, highlights):
    highlights = doc.highlights + highlights if highlights else []
    return {
        'annotation_id': annot.id,
        'comment': annot.comment,
        'responses': annot.responses,
        'name': doc.document_name,
        'metadata': doc.metadata,
        'text': doc.text,
        'highlights': highlights,
        'offsets': doc.offsets,
        'labels': doc.labels,
        'sentences': get_highlighted_sentences(doc.text, highlights, offsets=doc.offsets),
        'preview': _get_preview(doc),
    }


def get_annotation_by_id(project_name, annotation_id, username, subproject_name, *, highlights=None):
    if subproject_name:
        abu = AnnotationByUser.objects(project_name=project_name,
                                       username=username,
                                       annotation_id=annotation_id,
                                       subproject_name=subproject_name
                                       ).first()
    else:
        abu = AnnotationByUser.objects(project_name=project_name,
                                       username=username,
                                       annotation_id=annotation_id
                                       ).first()
    annot, doc = _get_or_create_annotation(abu)
    write_history(annotation_id, project_name, username, doc.document_name, how=HistoryHow.BY_ANNOT_ID,
                  subproject_name=subproject_name)
    if highlights is None:
        highlights = highlight_service.get_highlights(username, project_name)
    return _get_abu_response(annot, doc, highlights)


def get_next_annotation(project_name, username, subproject_name, *, highlights=None):
    if not (abu := get_next_abu(project_name, username, subproject_name)):
        return None
    annot, doc = _get_or_create_annotation(abu, set_state=AnnotationState.IN_PROGRESS)
    write_history(annot.id, project_name, username, doc.document_name, how=HistoryHow.NEXT,
                  subproject_name=subproject_name)
    if highlights is None:
        highlights = highlight_service.get_highlights(username, project_name)
    return _get_abu_response(annot, doc, highlights)


def _get_preview(doc):
    preview = []
    for offset in sorted(doc.offsets):
        preview.append(doc.text[offset.start:offset.end])
    return preview


def get_highlighted_sentences(text, highlights, offsets=None):
    sentences = []
    pat = None if not highlights else re.compile(rf"\b({'|'.join(re.escape(rx) for rx in highlights if rx)})\w*\b",
                                                 re.IGNORECASE)
    start = 0
    for line in text.split('\n'):
        sent_start = start
        sent_end = sent_start + len(line) + 1
        emphasize = False
        for offset in offsets or []:
            if sent_start <= offset.start < sent_end or sent_start <= offset.end < sent_end:
                emphasize = True
                break
        sentence = []
        if pat:
            m = None
            offset = 0
            for m in pat.finditer(line):
                sentence.append({
                    'text': text[sent_start + offset:m.start() + sent_start],
                    'emphasize': emphasize,
                    'highlight': False
                })
                sentence.append({
                    'text': text[m.start() + sent_start:m.end() + sent_start],
                    'emphasize': emphasize,
                    'highlight': True
                })
                offset = m.end()
            if m:
                sent_start = m.end() + sent_start
        sentence.append({
            'text': text[sent_start:sent_end],
            'emphasize': emphasize,
            'highlight': False,
        })
        sentences.append(sentence)
        start = sent_end
    return sentences


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
    annot.save()


def mark_annotation_completed(project_name, username, annotation_id):
    done_time = datetime.datetime.now()
    annot = get_annotation(annotation_id)
    annot.update_dates.append(done_time)
    annot.save()
    abu = AnnotationByUser.objects(
        username=username,
        project_name=project_name,
        annotation_id=annotation_id,
    ).first()
    abu.annotation_state = AnnotationState.DONE
    abu.save()
