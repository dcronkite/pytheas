import os

from pytheas.viewmodels.viewmodelbase import ViewModelBase


class HomeViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.corpus_path = self.request_dict.corpus_path

    def validate(self):
        if not self.corpus_path:
            self.error = 'Corpus path must be specified.'
        elif not os.path.exists(self.corpus_path):
            self.error = f'Path does not exist: {self.corpus_path}'
