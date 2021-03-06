import os

from pytheas.services import service
from pytheas.viewmodels.viewmodelbase import ViewModelBase


class HomeViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.corpus_path = self.request_dict.corpus_path
        self.name = self.request_dict.name
        self.project = self.request_dict.project_name
        self.previous_corpora = service.get_previous_corpora()
        self.previous_corpus_path = self.request_dict.previous_corpus_path

    def validate(self):
        self.corpus_path = self.corpus_path or self.previous_corpus_path
        if not self.corpus_path:
            self.error = 'Corpus path must be specified.'
        elif not os.path.exists(self.corpus_path):
            self.error = f'Path does not exist: {self.corpus_path}'
