import dataclasses
import datetime
import uuid

from domain.exceptions.deadline import DeadlineInThePastException
from domain.models.base import Base
from domain.values.task_name import TaskName
from domain.events.tasks import (
    TasksCategoryChanged,
    TaskUpdated,
    TaskCompleted,
    TaskUnCompleted,
)


@dataclasses.dataclass
class Task(Base):
    user_oid: uuid.UUID
    name: TaskName
    is_complete: bool
    deadline: datetime.datetime | None = dataclasses.field(default=None)
    category_oid: uuid.UUID | None = dataclasses.field(default=None)
    valid: bool = dataclasses.field(default=True)

    def __post_init__(self):
        if (
            self.valid
            and self.deadline is not None
            and self.deadline.timestamp() <= datetime.datetime.now().timestamp()
        ):
            raise DeadlineInThePastException(self.deadline)

    def __hash__(self):
        return hash(self.user_oid)

    def change_category(self, category_oid: uuid.UUID) -> None:
        self.register_event(
            TasksCategoryChanged(
                task_oid=self.oid,
                category_oid=category_oid,
            )
        )
        self.category_oid = category_oid

    def complete_task(self):
        self.is_complete = True
        self.register_event(
            TaskCompleted(
                task_oid=self.oid,
            )
        )

    def uncomplete_task(self):
        self.is_complete = False
        self.register_event(
            TaskUnCompleted(
                task_oid=self.oid,
            )
        )

    def update_task(
        self,
        new_category: uuid.UUID | None,
        new_name: TaskName,
        new_deadline: datetime.datetime | None,
    ) -> None:
        self.deadline = new_deadline
        self.name = new_name
        self.valid = True
        self.category_oid = new_category
        self.__post_init__()
        self.register_event(
            TaskUpdated(
                task_oid=self.oid,
                category_oid=new_category,
                name=new_name.as_generic_type(),
                deadline=new_deadline,
            )
        )
