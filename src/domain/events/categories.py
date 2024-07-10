import uuid
from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class NewCategoryCreated(BaseEvent):
    user_oid: uuid.UUID
    title: str


@dataclass
class CategoryUpdated(BaseEvent):
    category_oid: uuid.UUID
    title: str


@dataclass
class CategoryDeleted(BaseEvent):
    category_oid: uuid.UUID
