import uuid
from dataclasses import dataclass
import hashlib
from joserfc import jwt
import datetime

from domain.models.user import User
from domain.values.access_token import AccessToken
from domain.values.email import Email
from domain.values.password import Password
from infrastructure.repositories.users.base import BaseUserRepository
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.users import (
    UserWithThatEmailAlreadyExistsException,
    UserNotFoundException,
    UserNotAuthorizedException,
)


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    email: str
    password: str


@dataclass(frozen=True)
class CreateUserCommandHandler(CommandHandler[CreateUserCommand, User]):
    user_repository: BaseUserRepository

    async def handle(self, command: CreateUserCommand) -> User:
        if await self.user_repository.check_user_exists_by_email(email=command.email):
            raise UserWithThatEmailAlreadyExistsException(command.email)
        new_user = User.create_user(
            email=Email(value=command.email), password=Password(command.password)
        )
        await self.user_repository.add_user(new_user)
        return new_user


@dataclass(frozen=True)
class DeleteUserCommand(BaseCommand):
    user_oid: uuid.UUID


@dataclass(frozen=True)
class DeleteUserCommandHandler(CommandHandler[DeleteUserCommand, None]):
    user_repository: BaseUserRepository

    async def handle(self, command: DeleteUserCommand) -> None:
        user = await self.user_repository.get_user_by_oid(command.user_oid)
        if user is None:
            raise UserNotFoundException(command.user_oid)
        user.delete_user()
        await self.user_repository.delete_user(user_oid=command.user_oid)


@dataclass(frozen=True)
class SignInUserCommand(BaseCommand):
    email: str
    password: str


@dataclass(frozen=True)
class SignInUserCommandHandler(CommandHandler[SignInUserCommand, AccessToken]):
    user_repository: BaseUserRepository

    async def handle(self, command: SignInUserCommand) -> AccessToken:
        user = await self.user_repository.check_user_by_email(command.email)
        if (
            user is None
            or user[0] is None
            or user[1] != hashlib.sha256(command.password.encode("utf8")).hexdigest()
        ):
            raise UserNotAuthorizedException(command.email, command.password)
        return AccessToken(
            jwt.encode(
                {"alg": "HS256"},
                {
                    "sub": user[0],
                    "exp": datetime.datetime.now(datetime.UTC)
                    + datetime.timedelta(hours=1),
                },
                key="ok",
                algorithms=["HS256"],
            )
        )
