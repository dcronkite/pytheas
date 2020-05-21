from flask import session


def add_regex(regex: str):
    session['new_regex'] = regex
    session.setdefault('regexes', []).append(regex)


def get_regexes():
    return session.setdefault('regexes', [])


def remove_regex(regex: str):
    session['regexes'] = list(filter(lambda r: r != regex, session.get('regexes', [])))


def save_corpus_path(corpus_path: str):
    session['corpus_path'] = corpus_path
    session.setdefault('previous_corpus_paths', []).append(corpus_path)


def get_corpus_path():
    return session.get('corpus_path', '')


def get_previous_corpus_paths():
    return set(session.setdefault('previous_corpus_paths', []))
