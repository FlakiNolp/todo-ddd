import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Response
from punq import Container

from application.api.schemas import ErrorSchema
from application.api.users.schemas import (
    SignUpRequestSchema,
    SignUpResponseSchema,
    SignInRequestSchema,
    SignInResponseSchema,
)
from domain.exceptions.base import ApplicationException
from logic import init_container
from logic.commands.users import CreateUserCommand, SignInUserCommand
from logic.mediator.base import Mediator


router = APIRouter(tags=["users"], prefix="/user")


@router.get("/")
async def root():
    return {"Hello": "World"}


@router.post(
    "/sign-up",
    response_model=SignUpResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Регистрация нового пользователя, если пользователя с таким email не существует",
    responses={
        status.HTTP_201_CREATED: {"model": SignUpResponseSchema},
        status.HTTP_412_PRECONDITION_FAILED: {"model": ErrorSchema},
    },
)
async def sign_up(
    schema: SignUpRequestSchema, container: Container = Depends(init_container)
) -> SignUpResponseSchema:
    """
    Регистрация нового пользователя
    :param schema: SignUpRequestSchema
    :param container: None
    :return: SignUpResponseSchema
    """
    try:
        mediator: Mediator = container.resolve(Mediator)
        user, *_ = await mediator.handle_command(
            CreateUserCommand(email=schema.email, password=schema.password)
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )
    return SignUpResponseSchema.from_model(user=user)


@router.post(
    "/sign-in",
    response_model=SignInResponseSchema,
    status_code=status.HTTP_200_OK,
    description="Возращает jwt токены",
    responses={
        status.HTTP_200_OK: {"model": SignInResponseSchema},
        status.HTTP_412_PRECONDITION_FAILED: {"model": ErrorSchema},
    },
)
async def sign_in(
    schema: SignInRequestSchema,
    response: Response,
    container: Container = Depends(init_container),
) -> Response:
    """
    Аутентификация пользователя
    :param schema:
    :param container:
    :return: SignInResponseSchema
    """
    try:
        mediator: Mediator = container.resolve(Mediator)
        access_token, *_ = await mediator.handle_command(
            command=SignInUserCommand(email=schema.email, password=schema.password)
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exception.message},
        )
    response.status_code = 200
    response.set_cookie(
        key="access-token",
        value=access_token.value,
        expires=int(datetime.timedelta(hours=1).total_seconds()),
        httponly=True,
    )
    return response
    # return SignInResponseSchema.from_model(access_token)
