import datetime
import uuid
from dataclasses import dataclass

from domain.models.category import Category
from domain.models.task import Task
from domain.values.task_name import TaskName
from infrastructure.repositories.categories.base import BaseCategoryRepository
from infrastructure.repositories.tasks.base import BaseTaskRepository
from infrastructure.repositories.users.base import BaseUserRepository

from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.categories import CategoryNotFoundException
from logic.exceptions.users import UserNotFoundException
from logic.exceptions.tasks import TaskNotFoundException


@dataclass(frozen=True)
class GetAllTasksCommand(BaseCommand):
    user_oid: uuid.UUID


@dataclass(frozen=True)
class GetAllTasksCommandHandler(CommandHandler[GetAllTasksCommand, list[Task]]):
    task_repository: BaseTaskRepository
    user_repository: BaseUserRepository

    async def handle(self, command: GetAllTasksCommand) -> list[Task]:
        user = await self.user_repository.get_user_by_oid(command.user_oid)
        if user is None:
            raise UserNotFoundException(command.user_oid)
        tasks = await self.task_repository.get_tasks(command.user_oid)
        if tasks is None:
            return []
        return list(tasks)


@dataclass(frozen=True)
class CreateTaskCommand(BaseCommand):
    user_oid: uuid.UUID
    category_oid: uuid.UUID | None
    name: str
    is_complete: bool
    deadline: datetime.datetime | None


@dataclass(frozen=True)
class CreateTaskCommandHandler(CommandHandler[CreateTaskCommand, Task]):
    task_repository: BaseTaskRepository
    user_repository: BaseUserRepository
    category_repository: BaseCategoryRepository

    async def handle(self, command: CreateTaskCommand) -> Task:
        category: Category | None = None
        if command.category_oid is not None:
            category = await self.category_repository.get_category_by_oid(
                command.category_oid
            )
            if category is None:
                raise CategoryNotFoundException(command.category_oid)
        user = await self.user_repository.get_user_by_oid(command.user_oid)
        if user is None:
            raise UserNotFoundException(command.user_oid)
        task = Task(
            user_oid=user.oid,
            category_oid=category.oid if category else None,
            name=TaskName(command.name),
            is_complete=command.is_complete,
            deadline=(
                command.deadline.astimezone(datetime.timezone.utc)
                if command.deadline
                else None
            ),
        )
        user.create_new_task(task=task)
        await self.task_repository.add_task(task=task)
        return task


@dataclass(frozen=True)
class CompleteTaskCommand(BaseCommand):
    task_oid: uuid.UUID


@dataclass(frozen=True)
class CompleteTaskCommandHandler(CommandHandler[CompleteTaskCommand, None]):
    task_repository: BaseTaskRepository

    async def handle(self, command: CompleteTaskCommand):
        task = await self.task_repository.get_task_by_oid(command.task_oid)
        if task is None:
            raise TaskNotFoundException(command.task_oid)
        task.complete_task()
        await self.task_repository.complete_task(command.task_oid)


@dataclass(frozen=True)
class UnCompleteTaskCommand(BaseCommand):
    task_oid: uuid.UUID


@dataclass(frozen=True)
class UnCompleteTaskCommandHandler(CommandHandler[UnCompleteTaskCommand, None]):
    task_repository: BaseTaskRepository

    async def handle(self, command: UnCompleteTaskCommand):
        task = await self.task_repository.get_task_by_oid(command.task_oid)
        if task is None:
            raise TaskNotFoundException(command.task_oid)
        task.uncomplete_task()
        await self.task_repository.uncomplete_task(command.task_oid)


@dataclass(frozen=True)
class DeleteTaskCommand(BaseCommand):
    task_oid: uuid.UUID


@dataclass(frozen=True)
class DeleteTaskCommandHandler(CommandHandler[DeleteTaskCommand, None]):
    task_repository: BaseTaskRepository

    async def handle(self, command: DeleteTaskCommand):
        task = await self.task_repository.get_task_by_oid(command.task_oid)
        if task is None:
            raise TaskNotFoundException(command.task_oid)
        await self.task_repository.delete_task(command.task_oid)


@dataclass(frozen=True)
class ChangeCategoryTaskCommand(BaseCommand):
    task_oid: uuid.UUID
    category_oid: uuid.UUID


@dataclass(frozen=True)
class ChangeCategoryCommandHandler(CommandHandler[ChangeCategoryTaskCommand, None]):
    task_repository: BaseTaskRepository
    category_repository: BaseCategoryRepository

    async def handle(self, command: ChangeCategoryTaskCommand):
        category = await self.category_repository.get_category_by_oid(
            command.category_oid
        )
        if category is None:
            raise CategoryNotFoundException(command.category_oid)
        task = await self.task_repository.get_task_by_oid(command.task_oid)
        if task is None:
            raise TaskNotFoundException(command.task_oid)
        task.change_category(command.category_oid)
        await self.task_repository.change_category(
            category_oid=command.category_oid, task_oid=command.task_oid
        )


@dataclass(frozen=True)
class UpdateTaskCommand(BaseCommand):
    task_oid: uuid.UUID
    category_oid: uuid.UUID
    name: str
    deadline: datetime.datetime


@dataclass(frozen=True)
class UpdateTaskCommandHandler(CommandHandler[UpdateTaskCommand, None]):
    task_repository: BaseTaskRepository

    async def handle(self, command: UpdateTaskCommand):
        task = await self.task_repository.get_task_by_oid(command.task_oid)
        if task is None:
            raise TaskNotFoundException(command.task_oid)
        task.update_task(
            new_name=TaskName(command.name),
            new_deadline=command.deadline,
            new_category=command.category_oid,
        )
        await self.task_repository.update_task(
            task_oid=command.task_oid,
            category_oid=command.category_oid,
            name=command.name,
            deadline=command.deadline,
        )
