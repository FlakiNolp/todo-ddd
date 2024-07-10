import uuid
from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class NewUserCreated(BaseEvent):
    email: str
    password: str


@dataclass
class UserDeleted(BaseEvent):
    user_oid: uuid.UUID
