import dataclasses
import uuid
from typing import Iterable

from sqlalchemy import update, delete, select

from domain.models.category import Category as DomainCategory
from infrastructure.repositories.base_sqlalchemy_repository import (
    BaseSQLAlchemyRepository,
)
from infrastructure.repositories.categories.base import BaseCategoryRepository
from infrastructure.repositories.categories.converters import (
    convert_sqlalchemy_category_to_model,
)
from infrastructure.repositories.converters import Converter
from infrastructure.repositories.models import (
    Category as SQLAlchemyCategory,
    User as SQLAlchemyUser,
)


@dataclasses.dataclass
class SQLAlchemyCategoryRepository(BaseSQLAlchemyRepository, BaseCategoryRepository):
    async def add_category(self, category: DomainCategory) -> None:
        async with self._async_session_maker() as async_session:
            async_session.add(Converter.convert_from_model_to_sqlalchemy(category))
            await async_session.commit()

    async def update_category(
        self, category_oid: uuid.UUID, title: str
    ) -> DomainCategory | None:
        async with self._async_session_maker() as async_session:
            res = (
                (
                    await async_session.scalars(
                        update(SQLAlchemyCategory)
                        .filter(SQLAlchemyCategory.oid == category_oid)
                        .values(title=title)
                        .returning(SQLAlchemyCategory)
                    )
                )
                .unique()
                .one_or_none()
            )
            if res is None:
                return None
            await async_session.commit()
            return convert_sqlalchemy_category_to_model(res)

    async def delete_category(self, category_oid: uuid.UUID) -> None:
        async with self._async_session_maker() as async_session:
            res = (
                (
                    await async_session.scalars(
                        select(SQLAlchemyCategory).filter(
                            SQLAlchemyCategory.oid == category_oid
                        )
                    )
                )
                .unique()
                .one_or_none()
            )
            if res is None:
                return None
            await async_session.delete(res)
            await async_session.commit()

    async def get_categories(
        self, user_oid: uuid.UUID
    ) -> Iterable[DomainCategory] | None:
        async with self._async_session_maker() as async_session:
            res = (
                (
                    await async_session.scalars(
                        select(SQLAlchemyCategory)
                        .select_from(SQLAlchemyUser)
                        .join(
                            SQLAlchemyCategory, SQLAlchemyCategory.user_oid == user_oid
                        )
                    )
                )
                .unique()
                .all()
            )
            if res is None:
                return None
            return [convert_sqlalchemy_category_to_model(i) for i in res]

    async def get_category_by_oid(
        self, category_oid: uuid.UUID
    ) -> DomainCategory | None:
        async with self._async_session_maker() as async_session:
            res = (
                (
                    await async_session.scalars(
                        select(SQLAlchemyCategory).filter(
                            SQLAlchemyCategory.oid == category_oid
                        )
                    )
                )
                .unique()
                .one_or_none()
            )
            if res is None:
                return None
            return convert_sqlalchemy_category_to_model(res)
