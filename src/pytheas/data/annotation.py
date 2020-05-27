from dataclasses import dataclass

import persistent

from pytheas.data.annotation_label import AnnotationLabel
from pytheas.data.user import User


@dataclass
class Annotation(persistent.Persistent):
    label: AnnotationLabel
    source: User
    text: str
