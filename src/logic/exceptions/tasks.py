import uuid
from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(frozen=True, eq=False)
class TaskNotFoundException(LogicException):
    task_oid: uuid.UUID

    @property
    def message(self):
        return f"Задача с oid <{self.task_oid}> не найдена"
