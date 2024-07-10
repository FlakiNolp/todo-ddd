import abc
import dataclasses
import uuid

from domain.models.user import User


@dataclasses.dataclass
class BaseUserRepository(abc.ABC):
    @abc.abstractmethod
    async def check_user_exists_by_email(self, email: str) -> bool: ...
    @abc.abstractmethod
    async def get_user_by_oid(self, user_oid: uuid.UUID) -> User | None: ...
    @abc.abstractmethod
    async def add_user(self, user: User) -> None: ...
    @abc.abstractmethod
    async def delete_user(self, user_oid: uuid.UUID) -> None: ...
    @abc.abstractmethod
    async def check_user_by_email(self, email: str) -> tuple[str, str] | None: ...
