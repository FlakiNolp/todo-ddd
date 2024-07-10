import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from joserfc.jwt import Token
from punq import Container

from application.api.categories.dependencies import user_auth
from application.api.schemas import ErrorSchema
import application.api.categories.schemas as categories_schemas
from domain.exceptions.base import ApplicationException
from logic import init_container
from logic.commands.categories import (
    CreateCategoryCommand,
    GetAllCategoriesCommand,
    DeleteCategoryCommand,
    UpdateCategoryCommand,
)
from logic.mediator.base import Mediator


router = APIRouter(tags=["categories"], prefix="/category")


@router.get("/get-all", response_model=categories_schemas.GetAllResponseSchema)
async def get_all_categories(
    container: Container = Depends(init_container),
    authenticated: Token = Depends(user_auth),
) -> categories_schemas.GetAllResponseSchema:
    try:
        mediator: Mediator = container.resolve(Mediator)
        categories, *_ = await mediator.handle_command(
            GetAllCategoriesCommand(user_oid=authenticated.claims["sub"])
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
    return categories_schemas.GetAllResponseSchema.from_model(categories=categories)


@router.post("/create", response_model=categories_schemas.CreateCategoryResponseSchema)
async def create_category(
    schema: categories_schemas.CreateCategoryRequestSchema,
    container: Container = Depends(init_container),
    authenticated: Token = Depends(user_auth),
):
    try:
        mediator: Mediator = container.resolve(Mediator)
        category, *_ = await mediator.handle_command(
            CreateCategoryCommand(
                user_oid=authenticated.claims["sub"], title=schema.title
            )
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
    return categories_schemas.CreateCategoryResponseSchema.from_model(category=category)


@router.delete(
    "/delete", response_model=categories_schemas.DeleteCategoryResponseSchema
)
async def delete_category(
    schema: categories_schemas.DeleteCategoryRequestSchema,
    container: Container = Depends(init_container),
    authenticated: Token = Depends(user_auth),
):
    try:
        mediator: Mediator = container.resolve(Mediator)
        await mediator.handle_command(
            DeleteCategoryCommand(category_oid=schema.category_oid)
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
    return categories_schemas.DeleteCategoryResponseSchema.from_model()


@router.patch("/update", response_model=categories_schemas.UpdateCategoryResponseSchema)
async def update_category(
    schema: categories_schemas.UpdateCategoryRequestSchema,
    container: Container = Depends(init_container),
    authenticated: Token = Depends(user_auth),
):
    try:
        mediator: Mediator = container.resolve(Mediator)
        category, *_ = await mediator.handle_command(
            UpdateCategoryCommand(
                category_oid=schema.category_oid, new_title=schema.title
            )
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
    return categories_schemas.UpdateCategoryResponseSchema.from_model(category=category)
