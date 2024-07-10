import uuid
from pydantic import BaseModel

from domain.models.user import User
from domain.values.access_token import AccessToken


class SignUpRequestSchema(BaseModel):
    email: str
    password: str


class SignUpResponseSchema(BaseModel):
    oid: uuid.UUID
    email: str

    @classmethod
    def from_model(cls, user: User) -> "SignUpResponseSchema":
        return SignUpResponseSchema(
            oid=user.oid,
            email=user.email.as_generic_type(),
        )


class SignInRequestSchema(BaseModel):
    email: str
    password: str


class SignInResponseSchema(BaseModel):
    access_token: str

    @classmethod
    def from_model(cls, access_token: AccessToken) -> "SignInResponseSchema":
        return SignInResponseSchema(access_token=access_token.as_generic_type())
