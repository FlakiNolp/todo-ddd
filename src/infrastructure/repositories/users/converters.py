from typing import Mapping, Any

from domain.models.user import User
from domain.values.email import Email
from domain.values.password import HashedPassword


def convert_sqlalchemy_user_to_model(user_model: Mapping[str, Any]) -> User:
    return User(
        oid=user_model.oid,
        email=Email(user_model.email),
        password=HashedPassword(user_model.password),
    )
