from functools import lru_cache
from punq import Container, Scope
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine

from configs.config import ConfigSettings
from infrastructure.repositories.categories.base import BaseCategoryRepository
from infrastructure.repositories.categories.sqlalchemy import (
    SQLAlchemyCategoryRepository,
)
from infrastructure.repositories.models import Base
from infrastructure.repositories.tasks.base import BaseTaskRepository
from infrastructure.repositories.tasks.sqlalchemy import SQLAlchemyTaskRepository
from infrastructure.repositories.users.base import BaseUserRepository
from infrastructure.repositories.users.sqlalchemy import SQLAlchemyUserRepository
from logic.mediator.base import Mediator
from logic.commands.users import (
    CreateUserCommand,
    CreateUserCommandHandler,
    DeleteUserCommand,
    DeleteUserCommandHandler,
    SignInUserCommand,
    SignInUserCommandHandler,
)
from logic.commands.categories import (
    CreateCategoryCommand,
    CreateCategoryCommandHandler,
    DeleteCategoryCommand,
    DeleteCategoryCommandHandler,
    UpdateCategoryCommand,
    UpdateCategoryCommandHandler,
    GetAllCategoriesCommand,
    GetAllCategoriesCommandHandler,
)
from logic.commands.tasks import (
    CreateTaskCommand,
    CreateTaskCommandHandler,
    DeleteTaskCommand,
    DeleteTaskCommandHandler,
    UpdateTaskCommand,
    UpdateTaskCommandHandler,
    CompleteTaskCommand,
    CompleteTaskCommandHandler,
    UnCompleteTaskCommand,
    UnCompleteTaskCommandHandler,
    ChangeCategoryTaskCommand,
    ChangeCategoryCommandHandler,
    GetAllTasksCommand,
    GetAllTasksCommandHandler,
)


@lru_cache(None)
def init_container() -> Container:
    container = Container()

    container.register(CreateUserCommandHandler)
    container.register(DeleteUserCommandHandler)
    container.register(SignInUserCommandHandler)

    container.register(CreateCategoryCommandHandler)
    container.register(DeleteCategoryCommandHandler)
    container.register(UpdateCategoryCommandHandler)
    container.register(GetAllCategoriesCommandHandler)

    container.register(CreateTaskCommandHandler)
    container.register(DeleteTaskCommandHandler)
    container.register(UpdateTaskCommandHandler)
    container.register(CompleteTaskCommandHandler)
    container.register(UnCompleteTaskCommandHandler)
    container.register(ChangeCategoryCommandHandler)
    container.register(GetAllTasksCommandHandler)

    container.register(ConfigSettings, instance=ConfigSettings(), scope=Scope.singleton)

    def init_mediator() -> Mediator:
        mediator = Mediator()

        # Users
        mediator.register_command(
            CreateUserCommand, [container.resolve(CreateUserCommandHandler)]
        )
        mediator.register_command(
            DeleteUserCommand, [container.resolve(DeleteUserCommandHandler)]
        )
        mediator.register_command(
            SignInUserCommand, [container.resolve(SignInUserCommandHandler)]
        )

        # Categories
        mediator.register_command(
            CreateCategoryCommand, [container.resolve(CreateCategoryCommandHandler)]
        )
        mediator.register_command(
            DeleteCategoryCommand, [container.resolve(DeleteCategoryCommandHandler)]
        )
        mediator.register_command(
            UpdateCategoryCommand, [container.resolve(UpdateCategoryCommandHandler)]
        )
        mediator.register_command(
            GetAllCategoriesCommand, [container.resolve(GetAllCategoriesCommandHandler)]
        )

        # Tasks
        mediator.register_command(
            CreateTaskCommand, [container.resolve(CreateTaskCommandHandler)]
        )
        mediator.register_command(
            DeleteTaskCommand, [container.resolve(DeleteTaskCommandHandler)]
        )
        mediator.register_command(
            UpdateTaskCommand, [container.resolve(UpdateTaskCommandHandler)]
        )
        mediator.register_command(
            CompleteTaskCommand, [container.resolve(CompleteTaskCommandHandler)]
        )
        mediator.register_command(
            UnCompleteTaskCommand, [container.resolve(UnCompleteTaskCommandHandler)]
        )
        mediator.register_command(
            ChangeCategoryTaskCommand, [container.resolve(ChangeCategoryCommandHandler)]
        )
        mediator.register_command(
            GetAllTasksCommand, [container.resolve(GetAllTasksCommandHandler)]
        )

        return mediator

    async def migrate_db():
        config: ConfigSettings = container.resolve(ConfigSettings)
        async with create_async_engine(
            URL.create(
                drivername="postgresql+asyncpg",
                host=config.db_host,
                port=config.db_port,
                username=config.db_username,
                password=config.db_password,
                database=config.db_database,
            )
        ).begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    def init_user_sqlalchemy_repository():
        config: ConfigSettings = container.resolve(ConfigSettings)
        return SQLAlchemyUserRepository(
            config.db_host,
            config.db_port,
            config.db_username,
            config.db_password,
            config.db_database,
        )

    container.register(
        BaseUserRepository,
        factory=init_user_sqlalchemy_repository,
        scope=Scope.singleton,
    )

    def init_category_sqlalchemy_repository():
        config: ConfigSettings = container.resolve(ConfigSettings)
        return SQLAlchemyCategoryRepository(
            config.db_host,
            config.db_port,
            config.db_username,
            config.db_password,
            config.db_database,
        )

    container.register(
        BaseCategoryRepository,
        factory=init_category_sqlalchemy_repository,
        scope=Scope.singleton,
    )

    def init_task_sqlalchemy_repository():
        config: ConfigSettings = container.resolve(ConfigSettings)
        return SQLAlchemyTaskRepository(
            config.db_host,
            config.db_port,
            config.db_username,
            config.db_password,
            config.db_database,
        )

    container.register(
        BaseTaskRepository,
        factory=init_task_sqlalchemy_repository,
        scope=Scope.singleton,
    )

    container.register(Mediator, factory=init_mediator)

    return container
