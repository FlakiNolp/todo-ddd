import datetime
from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class DeadlineInThePastException(ApplicationException):
    deadline: datetime.datetime

    @property
    def message(self) -> str:
        return f"Срок выполнения задачи должен быть в будущем <{self.deadline}>"
