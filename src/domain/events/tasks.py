import datetime
import uuid
from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class NewTaskCreated(BaseEvent):
    user_oid: uuid.UUID
    category_oid: uuid.UUID | None
    name: str
    is_complete: bool
    deadline: datetime.datetime | None


@dataclass
class TaskDeleted(BaseEvent):
    task_oid: uuid.UUID


@dataclass
class TasksCategoryChanged(BaseEvent):
    task_oid: uuid.UUID
    category_oid: uuid.UUID


@dataclass
class TaskCompleted(BaseEvent):
    task_oid: uuid.UUID


@dataclass
class TaskUnCompleted(BaseEvent):
    task_oid: uuid.UUID


@dataclass
class TaskUpdated(BaseEvent):
    task_oid: uuid.UUID
    category_oid: uuid.UUID
    name: str
    deadline: datetime.datetime
