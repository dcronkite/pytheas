import enum

from mongoengine.base import BaseField


class EnumField(BaseField):
    def __init__(self, enum_class, **kwargs):
        self.enum_class = enum_class
        super().__init__(**kwargs)

    def to_python(self, value):
        try:
            self.enum_class(int(value))
        except (TypeError, ValueError):
            pass
        return value

    def to_mongo(self, value):
        if isinstance(value, int):
            return value
        return value.value

    def validate(self, value, **kwargs):
        if isinstance(value, enum.Enum):
            try:
                value = value.value
            except (TypeError, ValueError):
                self.error(f'{value} could not be converted to int')
        elif isinstance(value, int):
            try:
                value = self.enum_class(value)
            except ValueError:
                self.error(f'{value} could not be converted to {self.enum_class.__name__}')
        else:
            self.error(f'Unrecognized type: {value}; expected Enum or int')

    def prepare_query_value(self, op, value: enum.Enum):
        if value is None:
            return value

        return super().prepare_query_value(op, value.value)
