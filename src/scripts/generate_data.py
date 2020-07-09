import datetime
import json
import os
import string
import random
import pathlib
from collections import Counter

WORD_COUNTER = Counter()


def build_word():
    word = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
    WORD_COUNTER[word] += 1
    return word


def build_sentence():
    return ' '.join(build_word() for _ in range(random.randint(4, 12))) + '.'


def build_paragraph():
    return ' '.join(build_sentence() for _ in range(random.randint(1, 4)))


def build_document():
    return '\n'.join(build_paragraph() for _ in range(random.randint(1, 6)))


def build_schema():
    base_path = (pathlib.Path(__file__) / '..' / '..' / '..' / 'test' / 'generated').resolve()
    data_path = base_path / 'data'
    config_path = base_path / 'config'
    os.makedirs(data_path, exist_ok=True)
    os.makedirs(config_path, exist_ok=True)
    schema = {
        'connections': [
            {'name': 'directory',
             'path': str(data_path),
             }
        ],
        'documents': [

        ],
        'project': 'test_project',
        'start_date': datetime.datetime.now().strftime('%Y-%m-%d'),
        'end_date': (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y-%m-%d'),
        'labels': ['Yes', 'No'],
        'highlights': [],
        'annotation': {
            'annotators': [
                {
                    'name': 'admin',
                }
            ]
        }
    }
    for i in range(random.randint(10, 15)):
        doc_text = build_document()
        doc_name = f'document_{i}'
        start_offset = random.randint(0, len(doc_text) - 20)
        end_offset = random.randint(start_offset + 5, len(doc_text))
        with open(data_path / doc_name, 'w') as out:
            out.write(doc_text)
        document = {
            'name': doc_name,
            'metadata': {
                'name': doc_name,
            },
            'text': doc_text,
            'offsets': [
                {
                    'start': start_offset,
                    'end': end_offset,
                }
            ],
        }
        schema['documents'].append(document)
    # highlight 5 most common 'words'
    schema['highlights'] = [w for w, c in WORD_COUNTER.most_common(5)]

    # output json
    with open(config_path / 'example.json', 'w') as out:
        json.dump(schema, out)


if __name__ == '__main__':
    build_schema()
