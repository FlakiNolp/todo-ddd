import datetime
import uuid
from pydantic import BaseModel, Field

from domain.models.task import Task


class GetAllResponseSchema(BaseModel):
    tasks: list[dict[str, str | uuid.UUID | datetime.datetime | bool | None]]

    @classmethod
    def from_model(cls, tasks: list[Task]) -> "GetAllResponseSchema":
        return GetAllResponseSchema(
            tasks=[
                {
                    "oid": i.oid,
                    "name": i.name.as_generic_type(),
                    "category_oid": i.category_oid,
                    "is_complete": i.is_complete,
                    "deadline": i.deadline,
                }
                for i in tasks
            ],
        )


class CreateTaskRequestSchema(BaseModel):
    category_oid: uuid.UUID | None = Field(default=None)
    name: str
    deadline: datetime.datetime | None = Field(default=None)


class CreatTaskResponseSchema(BaseModel):
    task_oid: uuid.UUID
    category_oid: uuid.UUID | None
    name: str
    is_complete: bool
    deadline: datetime.datetime | None

    @classmethod
    def from_model(cls, task: Task) -> "CreatTaskResponseSchema":
        return CreatTaskResponseSchema(
            task_oid=task.oid,
            category_oid=task.category_oid,
            name=task.name.as_generic_type(),
            is_complete=task.is_complete,
            deadline=task.deadline,
        )


class DeleteTaskRequestSchema(BaseModel):
    task_oid: uuid.UUID


class DeleteTaskResponseSchema(BaseModel):
    @classmethod
    def from_model(cls) -> "DeleteTaskResponseSchema":
        return DeleteTaskResponseSchema()


class IsCompleteTaskRequestSchema(BaseModel):
    task_oid: uuid.UUID


class IsCompleteTaskResponseSchema(BaseModel):
    @classmethod
    def from_model(cls) -> "IsCompleteTaskResponseSchema":
        return IsCompleteTaskResponseSchema()


class IsUnCompleteTaskRequestSchema(BaseModel):
    task_oid: uuid.UUID


class IsUnCompleteTaskResponseSchema(BaseModel):
    @classmethod
    def from_model(cls) -> "IsUnCompleteTaskResponseSchema":
        return IsUnCompleteTaskResponseSchema()


class ChangeCategoryRequestSchema(BaseModel):
    task_oid: uuid.UUID
    category_oid: uuid.UUID


class ChangeCategoryResponseSchema(BaseModel):
    @classmethod
    def from_model(cls) -> "ChangeCategoryResponseSchema":
        return ChangeCategoryResponseSchema()


class UpdateTaskRequestSchema(BaseModel):
    task_oid: uuid.UUID
    category_oid: uuid.UUID | None = None
    name: str
    deadline: datetime.datetime | None = None


class UpdateTaskResponseSchema(BaseModel):

    @classmethod
    def from_model(cls) -> "UpdateTaskResponseSchema":
        return UpdateTaskResponseSchema()
