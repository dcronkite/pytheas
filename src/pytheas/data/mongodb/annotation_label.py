from dataclasses import dataclass

import persistent as persistent


@dataclass
class AnnotationLabel(persistent.Persistent):
    label: str
