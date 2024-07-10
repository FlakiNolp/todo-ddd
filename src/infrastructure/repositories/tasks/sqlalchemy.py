import dataclasses
import datetime
import uuid
from typing import Iterable

from sqlalchemy import update, delete, select

from domain.models.task import Task
from infrastructure.repositories.base_sqlalchemy_repository import (
    BaseSQLAlchemyRepository,
)
from infrastructure.repositories.converters import Converter
from infrastructure.repositories.models import (
    Task as SQLAlchemyTask,
    User as SQLAlchemyUser,
    Category as SQLAlchemyCategory,
)
from infrastructure.repositories.tasks.base import BaseTaskRepository
from infrastructure.repositories.tasks.converters import (
    convert_sqlalchemy_task_to_model,
)


@dataclasses.dataclass
class SQLAlchemyTaskRepository(BaseSQLAlchemyRepository, BaseTaskRepository):
    async def delete_task(self, task_oid: uuid.UUID) -> None:
        async with self._async_session_maker() as async_session:
            res = (
                (
                    await async_session.scalars(
                        select(SQLAlchemyTask).filter(SQLAlchemyTask.oid == task_oid)
                    )
                )
                .unique()
                .one_or_none()
            )
            if res is None:
                return None
            await async_session.delete(res)
            await async_session.commit()

    async def update_task(
        self,
        category_oid: uuid.UUID,
        name: str,
        deadline: datetime.datetime,
        task_oid: uuid.UUID,
    ) -> None:
        async with self._async_session_maker() as async_session:
            await async_session.scalars(
                update(SQLAlchemyTask)
                .filter(SQLAlchemyTask.oid == task_oid)
                .values(name=name, deadline=deadline, category_oid=category_oid)
                .returning(SQLAlchemyTask)
            )
            await async_session.commit()

    async def change_category(
        self, category_oid: uuid.UUID, task_oid: uuid.UUID
    ) -> None:
        async with self._async_session_maker() as async_session:
            await async_session.scalars(
                update(SQLAlchemyTask)
                .filter(SQLAlchemyTask.oid == task_oid)
                .values(category_oid=category_oid)
                .returning(SQLAlchemyTask)
            )
            await async_session.commit()

    async def complete_task(self, task_oid: uuid.UUID) -> None:
        async with self._async_session_maker() as async_session:
            await async_session.scalars(
                update(SQLAlchemyTask)
                .filter(SQLAlchemyTask.oid == task_oid)
                .values(is_complete=True)
                .returning(SQLAlchemyTask)
            )
            await async_session.commit()

    async def uncomplete_task(self, task_oid: uuid.UUID) -> None:
        async with self._async_session_maker() as async_session:
            await async_session.scalars(
                update(SQLAlchemyTask)
                .filter(SQLAlchemyTask.oid == task_oid)
                .values(is_complete=False)
                .returning(SQLAlchemyTask)
            )
            await async_session.commit()

    async def get_tasks(self, user_oid: uuid.UUID) -> Iterable[Task]:
        async with self._async_session_maker() as async_session:
            res = (
                (
                    await async_session.scalars(
                        select(SQLAlchemyTask)
                        .select_from(SQLAlchemyUser)
                        .join(
                            SQLAlchemyTask,
                            SQLAlchemyTask.user_oid == SQLAlchemyUser.oid,
                        )
                        .filter(SQLAlchemyUser.oid == user_oid)
                    )
                )
                .unique()
                .all()
            )
            return [convert_sqlalchemy_task_to_model(i) for i in res] if res else None

    async def get_tasks_by_category(
        self, user_oid: uuid.UUID, category_oid: uuid.UUID
    ) -> Iterable[Task]:
        async with self._async_session_maker() as async_session:
            res = (
                (
                    await async_session.scalars(
                        select(SQLAlchemyTask)
                        .select_from(SQLAlchemyUser)
                        .join(
                            SQLAlchemyTask,
                            SQLAlchemyTask.user_oid == SQLAlchemyUser.oid,
                        )
                        .join(
                            SQLAlchemyCategory,
                            SQLAlchemyCategory.oid == SQLAlchemyTask.category_oid,
                        )
                    )
                )
                .unique()
                .all()
            )
            return [convert_sqlalchemy_task_to_model(i) for i in res] if res else None

    async def add_task(self, task: Task) -> None:
        async with self._async_session_maker() as async_session:
            async_session.add(Converter.convert_from_model_to_sqlalchemy(task))
            await async_session.commit()

    async def get_task_by_oid(self, task_oid: uuid.UUID) -> Task | None:
        async with self._async_session_maker() as async_session:
            res = (
                await async_session.scalars(
                    select(SQLAlchemyTask)
                    .select_from(SQLAlchemyTask)
                    .filter(SQLAlchemyTask.oid == task_oid)
                )
            ).one_or_none()
            if res is None:
                return None
            return convert_sqlalchemy_task_to_model(res)
