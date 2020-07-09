import os
from dataclasses import dataclass

from pytheas.utils import sqlai


@dataclass
class Connection:
    name: str
    path: str = None
    driver: str = None
    server: str = None
    database: str = None
    name_col: str = None
    text_col: str = None

    def get(self, document_name):
        if self.path:
            return self._get_path(document_name)
        if self.driver:
            return self._get_from_sql(document_name)

    def _get_path(self, document_name):
        try:
            with open(os.path.join(self.path, document_name)) as fh:
                return fh.read()
        except Exception as e:
            print(e)
            return None

    def _get_from_sql(self, document_name):
        eng = sqlai.get_engine(self.name, driver=self.driver, server=self.server, database=self.database)
        for text in eng.execute(f'select {self.text_col} from {self.name} where {self.name_col} = "{document_name}"'):
            return text
        return None