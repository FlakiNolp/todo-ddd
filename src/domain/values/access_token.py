from dataclasses import dataclass

from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class AccessToken(BaseValueObject):
    value: str

    def validate(self): ...

    def as_generic_type(self) -> str:
        return self.value
