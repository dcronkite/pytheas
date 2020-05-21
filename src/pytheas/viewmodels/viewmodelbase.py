from typing import Optional

import flask
from flask import Request

from pytheas.utils import request_dict


class ViewModelBase:
    def __init__(self):
        self.request: Request = flask.request
        self.request_dict = request_dict.create('')

        self.error: Optional[str] = None

    def to_dict(self):
        return self.__dict__
