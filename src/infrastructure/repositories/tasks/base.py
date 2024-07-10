import abc
import dataclasses
import datetime
import uuid
from typing import Iterable

from domain.models.task import Task


@dataclasses.dataclass
class BaseTaskRepository(abc.ABC):
    @abc.abstractmethod
    async def add_task(self, task: Task) -> None: ...
    @abc.abstractmethod
    async def delete_task(self, task_oid: uuid.UUID) -> None: ...
    @abc.abstractmethod
    async def update_task(
        self,
        category_oid: uuid.UUID,
        name: str,
        deadline: datetime.datetime,
        task_oid: uuid.UUID,
    ) -> None: ...
    @abc.abstractmethod
    async def change_category(
        self, category_oid: uuid.UUID, task_oid: uuid.UUID
    ) -> None: ...
    @abc.abstractmethod
    async def complete_task(self, task_oid: uuid.UUID) -> None: ...
    @abc.abstractmethod
    async def uncomplete_task(self, task_oid: uuid.UUID) -> None: ...
    @abc.abstractmethod
    async def get_tasks(self, user_oid: uuid.UUID) -> Iterable[Task] | None: ...
    @abc.abstractmethod
    async def get_tasks_by_category(
        self, user_oid: uuid.UUID, category_oid: uuid.UUID
    ) -> Iterable[Task] | None: ...
    @abc.abstractmethod
    async def get_task_by_oid(self, task_oid: uuid.UUID) -> Task | None: ...
