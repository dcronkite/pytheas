import transaction
from flask import session

from pytheas.data.corpus import Corpus
from pytheas.data.zodb_setup import get_root


def add_regex(regex: str):
    session['new_regex'] = regex
    session.setdefault('regexes', []).append(regex)


def get_regexes():
    return session.setdefault('regexes', [])


def remove_regex(regex: str):
    session['regexes'] = list(filter(lambda r: r != regex, session.get('regexes', [])))


def save_corpus_path(name: str, corpus_path: str, project: str):
    c = Corpus(name=name, path=corpus_path, project=project)
    get_root('corpora')[c.name] = c
    transaction.commit()
    session['corpus_path'] = c


def get_corpus_path():
    return session.get('corpus_path', '')


def get_previous_corpora():
    return list(get_root('corpora').values())
