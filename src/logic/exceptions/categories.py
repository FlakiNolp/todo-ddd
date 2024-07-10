import uuid
from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(frozen=True, eq=False)
class CategoryNotFoundException(LogicException):
    category_oid: uuid.UUID

    @property
    def message(self):
        return f"Категория с oid <{self.category_oid}> не найдена"
