import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from joserfc.jwt import Token
from punq import Container

from application.api.categories.dependencies import user_auth
from application.api.schemas import ErrorSchema
import application.api.tasks.schemas as tasks_schemas
from domain.exceptions.base import ApplicationException
from logic import init_container
from logic.commands.tasks import (
    CreateTaskCommand,
    GetAllTasksCommand,
    DeleteTaskCommand,
    CompleteTaskCommand,
    UnCompleteTaskCommand,
    ChangeCategoryTaskCommand,
    UpdateTaskCommand,
)
from logic.mediator.base import Mediator


router = APIRouter(tags=["tasks"], prefix="/task")


@router.get("/get-all", response_model=tasks_schemas.GetAllResponseSchema)
async def get_all_tasks(
    container: Container = Depends(init_container),
    authenticated: Token = Depends(user_auth),
) -> tasks_schemas.GetAllResponseSchema:
    try:
        mediator: Mediator = container.resolve(Mediator)
        tasks, *_ = await mediator.handle_command(
            GetAllTasksCommand(user_oid=authenticated.claims["sub"])
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
    return tasks_schemas.GetAllResponseSchema.from_model(tasks=tasks)


@router.post("/create", response_model=tasks_schemas.CreatTaskResponseSchema)
async def create_tasks(
    schema: tasks_schemas.CreateTaskRequestSchema,
    container: Container = Depends(init_container),
    authenticated: Token = Depends(user_auth),
):
    try:
        mediator: Mediator = container.resolve(Mediator)
        task, *_ = await mediator.handle_command(
            CreateTaskCommand(
                user_oid=authenticated.claims["sub"],
                category_oid=schema.category_oid,
                name=schema.name,
                is_complete=False,
                deadline=schema.deadline,
            )
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
    return tasks_schemas.CreatTaskResponseSchema.from_model(task=task)


@router.delete("/delete", response_model=tasks_schemas.DeleteTaskResponseSchema)
async def delete_task(
    schema: tasks_schemas.DeleteTaskRequestSchema,
    container: Container = Depends(init_container),
    authenticated: Token = Depends(user_auth),
):
    try:
        mediator: Mediator = container.resolve(Mediator)
        await mediator.handle_command(DeleteTaskCommand(task_oid=schema.task_oid))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
    return tasks_schemas.DeleteTaskResponseSchema.from_model()


@router.patch("/complete", response_model=tasks_schemas.IsCompleteTaskResponseSchema)
async def complete_task(
    schema: tasks_schemas.IsCompleteTaskRequestSchema,
    container: Container = Depends(init_container),
    authenticated: Token = Depends(user_auth),
):
    try:
        mediator: Mediator = container.resolve(Mediator)
        await mediator.handle_command(CompleteTaskCommand(task_oid=schema.task_oid))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
    return tasks_schemas.IsCompleteTaskResponseSchema.from_model()


@router.patch(
    "/uncomplete", response_model=tasks_schemas.IsUnCompleteTaskResponseSchema
)
async def uncomplete_task(
    schema: tasks_schemas.IsUnCompleteTaskRequestSchema,
    container: Container = Depends(init_container),
    authenticated: Token = Depends(user_auth),
):
    try:
        mediator: Mediator = container.resolve(Mediator)
        await mediator.handle_command(UnCompleteTaskCommand(task_oid=schema.task_oid))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
    return tasks_schemas.IsCompleteTaskResponseSchema.from_model()


@router.patch(
    "/change-category", response_model=tasks_schemas.ChangeCategoryResponseSchema
)
async def change_category(
    schema: tasks_schemas.ChangeCategoryRequestSchema,
    container: Container = Depends(init_container),
    authenticated: Token = Depends(user_auth),
):
    try:
        mediator: Mediator = container.resolve(Mediator)
        await mediator.handle_command(
            ChangeCategoryTaskCommand(
                task_oid=schema.task_oid, category_oid=schema.category_oid
            )
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
    return tasks_schemas.ChangeCategoryResponseSchema.from_model()


@router.patch("/update", response_model=tasks_schemas.UpdateTaskResponseSchema)
async def update_category(
    schema: tasks_schemas.UpdateTaskRequestSchema,
    container: Container = Depends(init_container),
    authenticated: Token = Depends(user_auth),
):
    try:
        mediator: Mediator = container.resolve(Mediator)
        category, *_ = await mediator.handle_command(
            UpdateTaskCommand(
                task_oid=schema.task_oid,
                category_oid=schema.category_oid,
                name=schema.name,
                deadline=schema.deadline,
            )
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
    return tasks_schemas.UpdateTaskResponseSchema.from_model()
