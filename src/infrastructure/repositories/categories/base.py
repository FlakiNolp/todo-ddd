import abc
import dataclasses
import uuid
from typing import Iterable

from domain.models.category import Category


@dataclasses.dataclass
class BaseCategoryRepository(abc.ABC):
    @abc.abstractmethod
    async def add_category(self, category: Category) -> None: ...
    @abc.abstractmethod
    async def update_category(
        self, category_oid: uuid.UUID, name: str
    ) -> Category | None: ...
    @abc.abstractmethod
    async def delete_category(self, category_oid: uuid.UUID) -> None: ...
    @abc.abstractmethod
    async def get_categories(
        self, user_oid: uuid.UUID
    ) -> Iterable[Category] | None: ...
    @abc.abstractmethod
    async def get_category_by_oid(self, category_oid: uuid.UUID) -> Category | None: ...
