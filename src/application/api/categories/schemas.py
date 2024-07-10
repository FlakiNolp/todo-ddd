import uuid
from pydantic import BaseModel

from domain.models.category import Category


class GetAllResponseSchema(BaseModel):
    categories: list[dict[str, str | uuid.UUID]]

    @classmethod
    def from_model(cls, categories: list[Category]) -> "GetAllResponseSchema":
        return GetAllResponseSchema(
            categories=[
                {"oid": i.oid, "title": i.title.as_generic_type()} for i in categories
            ],
        )


class CreateCategoryRequestSchema(BaseModel):
    title: str


class CreateCategoryResponseSchema(BaseModel):
    category_oid: uuid.UUID
    title: str

    @classmethod
    def from_model(cls, category: Category) -> "CreateCategoryResponseSchema":
        return CreateCategoryResponseSchema(
            category_oid=category.oid,
            title=category.title.as_generic_type(),
        )


class DeleteCategoryRequestSchema(BaseModel):
    category_oid: uuid.UUID


class DeleteCategoryResponseSchema(BaseModel):

    @classmethod
    def from_model(cls) -> "DeleteCategoryResponseSchema":
        return DeleteCategoryResponseSchema()


class UpdateCategoryRequestSchema(BaseModel):
    category_oid: uuid.UUID
    title: str


class UpdateCategoryResponseSchema(BaseModel):
    category_oid: uuid.UUID
    title: str

    @classmethod
    def from_model(cls, category: Category) -> "UpdateCategoryResponseSchema":
        return UpdateCategoryResponseSchema(
            category_oid=category.oid,
            title=category.title.as_generic_type(),
        )
