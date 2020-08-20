import enum


class AnnotationState(enum.Enum):
    READY = 0
    IN_PROGRESS = 1
    DONE = 2
    DELETED = 3
    ON_HOLD = 4
    NOT_READY = 5
    SKIPPED = 6
