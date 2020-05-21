from pytheas.viewmodels.viewmodelbase import ViewModelBase


class HomeViewModel(ViewModelBase):
    def __init__(self, corpus_path: str):
        super().__init__()

        self.corpus_path = corpus_path
