import uuid
from dataclasses import dataclass

from domain.models.category import Category
from domain.values.category_title import CategoryTitle
from infrastructure.repositories.categories.base import BaseCategoryRepository
from infrastructure.repositories.users.base import BaseUserRepository
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.users import UserNotFoundException
from logic.exceptions.categories import CategoryNotFoundException


@dataclass(frozen=True)
class GetAllCategoriesCommand(BaseCommand):
    user_oid: uuid.UUID


@dataclass(frozen=True)
class GetAllCategoriesCommandHandler(
    CommandHandler[GetAllCategoriesCommand, list[Category]]
):
    category_repository: BaseCategoryRepository
    user_repository: BaseUserRepository

    async def handle(self, command: GetAllCategoriesCommand) -> list[Category]:
        user = await self.user_repository.get_user_by_oid(command.user_oid)
        if user is None:
            raise UserNotFoundException(command.user_oid)
        categories = await self.category_repository.get_categories(command.user_oid)
        if categories is None:
            return []
        return list(categories)


@dataclass(frozen=True)
class CreateCategoryCommand(BaseCommand):
    user_oid: uuid.UUID
    title: str


@dataclass(frozen=True)
class CreateCategoryCommandHandler(CommandHandler[CreateCategoryCommand, Category]):
    category_repository: BaseCategoryRepository
    user_repository: BaseUserRepository

    async def handle(self, command: CreateCategoryCommand) -> Category:
        user = await self.user_repository.get_user_by_oid(command.user_oid)
        if user is None:
            raise UserNotFoundException(command.user_oid)
        category = Category(
            user_oid=command.user_oid, title=CategoryTitle(command.title)
        )
        user.create_new_category(category=category)
        await self.category_repository.add_category(category=category)
        return category


@dataclass(frozen=True)
class UpdateCategoryCommand(BaseCommand):
    category_oid: uuid.UUID
    new_title: str


@dataclass(frozen=True)
class UpdateCategoryCommandHandler(CommandHandler[UpdateCategoryCommand, Category]):
    category_repository: BaseCategoryRepository

    async def handle(self, command: UpdateCategoryCommand):
        category = await self.category_repository.update_category(
            command.category_oid, command.new_title
        )
        if category is None:
            raise CategoryNotFoundException(command.category_oid)
        return category


@dataclass(frozen=True)
class DeleteCategoryCommand(BaseCommand):
    category_oid: uuid.UUID


@dataclass(frozen=True)
class DeleteCategoryCommandHandler(CommandHandler[DeleteCategoryCommand, None]):
    category_repository: BaseCategoryRepository

    async def handle(self, command: DeleteCategoryCommand):
        category = await self.category_repository.get_category_by_oid(
            category_oid=command.category_oid
        )
        if category is None:
            raise CategoryNotFoundException(command.category_oid)
        await self.category_repository.delete_category(
            category_oid=command.category_oid
        )
