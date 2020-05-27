from dataclasses import dataclass

import persistent as persistent


@dataclass
class Corpus(persistent.Persistent):
    name: str
    path: str
    project: str
