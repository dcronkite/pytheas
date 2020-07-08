from pytheas.services import admin_service
from pytheas.viewmodels.viewmodelbase import ViewModelBase


class AdminViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.tasks = admin_service.get_tasks()
        self.chosen_task = self.request_dict.chosen_task

    def validate(self):
        return bool(self.chosen_task)
