from dataclasses import dataclass
import re
import hashlib

from domain.values.base import BaseValueObject
from domain.exceptions.password import PasswordValidationException


@dataclass(frozen=True)
class Password(BaseValueObject):
    value: str

    def validate(self):
        if re.search("[a-z]", self.value) is None:
            raise PasswordValidationException("буквы нижнего регистра")
        elif re.search("[A-Z]", self.value) is None:
            raise PasswordValidationException("буквы верхнего регистра")
        if re.search("[0-9]", self.value) is None:
            raise PasswordValidationException("цифры")
        if re.search(r"\W", self.value) is None:
            raise PasswordValidationException("специальные символы")
        if len(self.value) < 6:
            raise PasswordValidationException("минимум 6 символов")

    def as_generic_type(self) -> str:
        return hashlib.sha256(self.value.encode("utf8")).hexdigest()


@dataclass(frozen=True)
class HashedPassword(BaseValueObject):
    value: str

    def validate(self): ...

    def as_generic_type(self) -> str:
        return self.value
