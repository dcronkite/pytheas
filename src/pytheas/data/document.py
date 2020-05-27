from dataclasses import dataclass, field
from typing import List

import persistent

from pytheas.data.annotation import Annotation
from pytheas.data.corpus import Corpus


@dataclass
class Document(persistent.Persistent):
    name: str
    length: int
    annotations: List[Annotation] = field(default_factory=list)
    corpora: List[Corpus] = field(default_factory=list)

    def add_annotation(self, annot: Annotation):
        self.annotations.append(annot)
        self._p_changed = True

    def add_corpus(self, corpus: Corpus):
        self.corpora.append(corpus)
