import os
import pathlib
import re
from dataclasses import dataclass, field
from typing import List

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
    metadata: List[str] = field(default_factory=list)
    include_regex: str = None
    exclude_regex: str = None

    @property
    def include_rx(self):
        return re.compile(self.include_regex, re.I) if self.include_regex else None

    @property
    def exclude_rx(self):
        return re.compile(self.exclude_regex, re.I) if self.exclude_regex else None

    @property
    def extra_columns(self):
        if not self.metadata:
            return ''
        return ', '.join([''] + self.metadata)

    @property
    def tablename_safe(self):
        return self.tablename or self.name

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
                f"select {self.text_col} from {self.tablename_safe} where {self.name_col} = '{document_name}'"
        ):
            return text[0]
        return None

    def _join_metadata(self, metadata):
        return {x: y for x, y in zip(self.metadata, metadata)}

    def iterate(self, include_regex=None, exclude_regex=None):
        for name, text, metadata in self._get_next():
            if exclude_regex and exclude_regex.search(text):
                continue
            elif self.exclude_rx and self.exclude_rx.search(text):
                continue
            if include_regex and include_regex.search(text):
                pass
            elif self.include_rx and self.include_rx.search(text):
                pass
            elif include_regex or self.include_rx:
                continue
            else:
                pass
            yield name, text, self._join_metadata(metadata)

    def _get_next(self):
        if self.path:
            yield from self._get_next_from_path()
        if self.server:
            yield from self._get_next_from_sql()

    def _get_next_from_path(self):
        for f in (f for f in pathlib.Path('*') if f.is_file()):
            try:
                with open(f) as fh:
                    yield f.name, fh.read(), []
            except Exception as e:
                print(e)

    def _get_next_from_sql(self):
        for name, text, *metadata in self._get_engine().execute(
                f'select {self.name_col}, {self.text_col} {self.extra_columns}'
                f' from {self.tablename_safe} {self.ad_hoc_safe}'
        ):
            yield name, text, metadata

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

    def test_query(self):
        if self.path:
            path = pathlib.Path(self.path)
            if path.exists():
                return True, f'Path contains {len(list(path.glob("*")))} files.'
            else:
                return False, 'Path does not exist'
        if self.server:
            try:
                ad_hoc_safe = self.ad_hoc_safe
            except ValueError:
                return False, 'Where clause considered unsafe.'
            try:
                _ = self._get_engine().execute(
                    f'select {self.name_col}, {self.text_col} {self.extra_columns}'
                    f' from {self.tablename_safe} {ad_hoc_safe}'
                ).first()
            except Exception as e:
                return False, str(e)
            try:
                cnt = self._get_engine().execute(
                    f'select count(*) from {self.tablename_safe} {ad_hoc_safe}'
                ).first()
            except Exception as e:
                return False, str(e)
            return True, f'Table contains {cnt[0]} records.'
        return False, 'Must specify either Directory or Database'
