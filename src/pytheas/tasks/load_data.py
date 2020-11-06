import datetime
import json
import os
import uuid

import jsonschema

from pytheas import app
from pytheas.data.annotation_by_user import AnnotationByUser
from pytheas.data.annotation_state import AnnotationState
from pytheas.data.documents import Document
from pytheas.data.highlight import Highlight
from pytheas.data.projects import Project
from pytheas.data.uploads import Upload
from pytheas.tasks.connection import Connection
from pytheas.tasks.schema import get_schema


def setup_connections(*connections):
    conns = []
    for connection in connections:
        conns.append(
            Connection(**connection)
        )
    return conns


def resolve_expiration_date(*dates):
    for date in dates:
        if date:
            return date
    return datetime.datetime.now() + datetime.timedelta(days=91)


def add_documents_to_user(upload: Upload, project_name: str, subproject_name: str, username: str, document_list,
                          connections, labels=None, order=0, end_date=None, highlights=None):
    if not highlights:
        highlights = list()
    for document in document_list:
        name = document['name']
        text = document.get('text', None)
        if not text:
            for connection in connections:
                text = connection.get(name)
                if text:
                    break
            else:
                raise ValueError(f'Unable to locate document {name}')
        doc = Document(
            document_name=name,
            metadata=document.get('metadata', dict()),
            username=username,
            text=str(text),
            project_name=project_name,
            order=document.get('order', order),
            highlights=document.get('highlights', list()) + highlights,
            expiration_date=resolve_expiration_date(document.get('expiration_date', None), end_date),
            offsets=[Highlight(**offset) for offset in document.get('offsets', list())],
            labels=document.get('labels', labels)
        )
        doc.save()
        upload.document_ids.append(doc.id)
        abu = AnnotationByUser(
            username=username,
            document_id=doc.id,
            project_name=project_name,
            subproject_name=subproject_name,
            annotation_state=AnnotationState.READY,
        )
        abu.save()


def _load_json_to_database(filepath, upload: Upload):
    with open(filepath) as fh:
        data = json.load(fh)
    try:
        jsonschema.validate(data, get_schema())
    except Exception as e:
        print(e)
        return False

    # setup connections
    connections = setup_connections(*data['connections'])

    # get project
    try:
        project = Project.objects(project_name=data['project']).first()
    except Exception as e:
        raise ValueError(f'Project does not exist: {data["project"]}, {e}')
    if not project:
        raise ValueError(f'Project does not exist: {data["project"]}. Please create project first.')

    subproject_name = data.get('subproject', f'{project.name}_{uuid.uuid4()}')
    project.subprojects.append(subproject_name)
    project.save()
    labels = data.get('labels', None)
    highlights = data.get('highlights', list())
    documents = data.get('documents', [])
    document_index = 0
    start_index = 0
    end_index = None
    n_users = len(data['annotation']['annotators'])
    for user_index, user in enumerate(data['annotation']['annotators']):
        if user['name'] not in project.usernames:
            raise ValueError(f'User not part of project: {user["name"]}, {project.name}')
        add_documents_to_user(upload,
                              project.name,
                              subproject_name,
                              user['name'],
                              user.get('documents', []),
                              connections,
                              labels=labels,
                              end_date=project.end_date,
                              highlights=highlights)
        add_documents_to_user(upload,
                              project.name,
                              subproject_name,
                              user['name'],
                              data.get('irr_documents', []),
                              connections,
                              labels=labels,
                              end_date=project.end_date,
                              highlights=highlights
                              )
        if n_users == user_index + 1:  # last user
            end_index = None
        elif 'number' in user:
            start_index = document_index
            end_index = document_index + user['number']
            document_index = end_index
        elif 'percent' in user:
            increment = round(user['percent'] * len(documents))
            start_index = document_index
            end_index = document_index + increment
            document_index = end_index
        add_documents_to_user(upload,
                              project.name,
                              subproject_name,
                              user['name'],
                              documents[start_index:end_index],
                              connections,
                              labels=labels,
                              end_date=project.end_date,
                              highlights=highlights
                              )
    return True


def load_data():
    with app.app_context():
        data_dir = app.config['DATA_DIR']
        names = {upload.name for upload in Upload.objects(completed=True)}
        # TODO: handle incomplete uploads
        print(data_dir)
        for root, dirs, files in os.walk(data_dir):
            for file in files:
                print(file)
                if not file.endswith('json'):
                    continue
                filename = file[:-5]
                print(names)
                if filename not in names:
                    upload = Upload(
                        name=filename,
                        source_path=root,
                    )
                    print(upload)
                    upload.save()
                    try:
                        result = _load_json_to_database(os.path.join(root, file), upload)
                    except Exception as e:
                        print(f'Failed to load {file} at {root} due to {e}')
                        raise e
                        upload.errors.append(str(e))
                        upload.save()
                        continue
                    if result:
                        upload.mark_completed()
                        upload.save()
                        print(f'Done {upload}')
                    else:
                        print(f'Upload failed for {filename}')
