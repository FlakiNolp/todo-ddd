import uuid
from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(frozen=True, eq=False)
class UserWithThatEmailAlreadyExistsException(LogicException):
    email: str

    @property
    def message(self):
        return f"Пользователь с почтой <{self.email}> уже существует"


@dataclass(frozen=True, eq=False)
class UserNotFoundException(LogicException):
    user_oid: uuid.UUID

    @property
    def message(self):
        return f"Пользователь с oid <{self.user_oid}> не найден"


@dataclass(frozen=True, eq=False)
class UserNotAuthorizedException(LogicException):
    email: str
    password: str

    @property
    def message(self):
        return "Неверная почта или пароль"
