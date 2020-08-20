import os
import pathlib
import re
from dataclasses import dataclass

from pytheas.utils import sqlai


@dataclass
class Connection:
    name: str  # just the name of this connection
    tablename: str = None  # only for tablename
    path: str = None  # complete path
    driver: str = None
    server: str = None
    database: str = None
    name_col: str = None
    text_col: str = None
    ad_hoc_clause: str = None  # arbitrary where clause

    def get(self, document_name):
        if self.path:
            return self._get_path(document_name)
        if self.driver:
            return self._get_from_sql(document_name)

    def _get_engine(self):
        return sqlai.get_engine(self.name, driver=self.driver, server=self.server, database=self.database)

    def _get_path(self, document_name):
        try:
            with open(os.path.join(self.path, document_name)) as fh:
                return fh.read()
        except Exception as e:
            print(e)
            return None

    def _get_from_sql(self, document_name):
        eng = self._get_engine()
        for text in eng.execute(
                f"select {self.text_col} from {self.tablename or self.name} where {self.name_col} = '{document_name}'"
        ):
            return text[0]
        return None

    def iterate(self, include_regex=None, exclude_regex=None):
        if exclude_regex:
            exclude_regex = re.compile('({})'.format('|'.join(exclude_regex)), re.I)
        if include_regex:
            include_regex = re.compile('({})'.format('|'.join(include_regex)), re.I)
        for name, text in self._get_next():
            if exclude_regex and exclude_regex.search(text):
                continue
            if not include_regex or include_regex.search(text):
                yield name, text

    def _get_next(self):
        if self.path:
            yield from self._get_next_from_path()
        if self.server:
            yield from self._get_next_from_sql()

    def _get_next_from_path(self):
        for f in (f for f in pathlib.Path('*') if f.is_file()):
            try:
                with open(f) as fh:
                    yield f.name, fh.read()
            except Exception as e:
                print(e)

    def _get_next_from_sql(self):
        for name, text in self._get_engine().execute(
                f'select {self.name_col}, {self.text_col} from {self.tablename or self.name} {self.ad_hoc_safe}'
        ):
            yield name, text

    @property
    def ad_hoc_safe(self):
        ad_hoc = ';'.split(self.ad_hoc_clause)[0].strip()
        ad_hoc_lower = ad_hoc.lower()
        if (not ad_hoc_lower.startswith('where') or 'drop' in ad_hoc_lower
                or 'delete' in ad_hoc_lower or ad_hoc_lower.startswith('update')
                or 'declare' in ad_hoc_lower or 'exec' in ad_hoc_lower
        ):
            raise ValueError(f'Suspected SQL injection query: {ad_hoc}')
        return ad_hoc
