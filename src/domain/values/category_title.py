from dataclasses import dataclass

from domain.exceptions.category_title import EmptyTextException, TitleTooLongException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class CategoryTitle(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTextException()
        if len(self.value) > 255:
            raise TitleTooLongException(self.value)

    def as_generic_type(self):
        return self.value
