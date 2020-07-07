from dataclasses import dataclass

import persistent

from pytheas.data.mongodb.annotation_label import AnnotationLabel
from pytheas.data.mongodb.user import User


@dataclass
class Annotation(persistent.Persistent):
    label: AnnotationLabel
    source: User
    text: str
