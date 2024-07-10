import dataclasses
import uuid

from sqlalchemy import delete, select

from domain.models.user import User as DomainUser, User
from infrastructure.repositories.base_sqlalchemy_repository import (
    BaseSQLAlchemyRepository,
)
from infrastructure.repositories.converters import Converter
from infrastructure.repositories.users.base import BaseUserRepository
from infrastructure.repositories.models import User as SQLAlchemyUser
from infrastructure.repositories.users.converters import (
    convert_sqlalchemy_user_to_model,
)


@dataclasses.dataclass
class SQLAlchemyUserRepository(BaseSQLAlchemyRepository, BaseUserRepository):
    async def check_user_exists_by_email(self, email: str) -> bool:
        async with self._async_session_maker() as async_session:
            res = (
                await async_session.scalars(
                    select(SQLAlchemyUser).filter(SQLAlchemyUser.email == email)
                )
            ).one_or_none()
            if res is None:
                return False
            return True

    async def get_user_by_oid(self, user_oid: uuid.UUID) -> DomainUser | None:
        async with self._async_session_maker() as async_session:
            res = (
                await async_session.scalars(
                    select(SQLAlchemyUser).filter(SQLAlchemyUser.oid == user_oid)
                )
            ).one_or_none()
            if res is None:
                return None
            return convert_sqlalchemy_user_to_model(res)

    async def add_user(self, user: DomainUser) -> None:
        async with self._async_session_maker() as async_session:
            async_session.add(Converter.convert_from_model_to_sqlalchemy(user))
            await async_session.commit()

    async def delete_user(self, user_oid: uuid.UUID) -> None:
        async with self._async_session_maker() as async_session:
            await async_session.scalars(
                delete(SQLAlchemyUser).filter(SQLAlchemyUser.oid == user_oid)
            )
            await async_session.commit()

    async def check_user_by_email(self, email: str) -> tuple[str, str] | None:
        async with self._async_session_maker() as async_session:
            res = (
                await async_session.scalars(
                    select(SQLAlchemyUser).filter(SQLAlchemyUser.email == email)
                )
            ).one_or_none()
            if res is None:
                return None
            return str(res.oid), res.password
