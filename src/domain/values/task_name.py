from dataclasses import dataclass

from domain.exceptions.category_title import EmptyTextException, TitleTooLongException
from domain.values.base import BaseValueObject
from domain.exceptions.email import EmailValidationException


@dataclass(frozen=True)
class TaskName(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTextException()
        if len(self.value) > 150:
            raise TitleTooLongException(self.value)

    def as_generic_type(self):
        return self.value
