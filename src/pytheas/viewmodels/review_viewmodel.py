from pytheas import service
from pytheas.viewmodels.viewmodelbase import ViewModelBase


class ReviewViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.regexes = service.get_regexes()
        self.new_regex = self.request_dict.new_regex
        self.remove_regex = self.request_dict.remove

    def reset(self):
        self.new_regex = ''
        self.remove_regex = None
        self.regexes = service.get_regexes()
