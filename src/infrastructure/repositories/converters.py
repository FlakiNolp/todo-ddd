from typing import ForwardRef, Type

import sqlalchemy.orm
from sqlalchemy.orm import class_mapper

from domain.models.base import Base as DomainBase
from domain.models.user import User as DomainUser
from domain.models.task import Task as DomainTask
from domain.models.category import Category as DomainCategory
from domain.values.base import BaseValueObject
from domain.values.category_title import CategoryTitle
from domain.values.email import Email
from domain.values.password import Password
from domain.values.task_name import TaskName
from infrastructure.repositories.models import Base as SQLAlchemyBaseModel
from infrastructure.repositories.models import User as SQLAlchemyUser
from infrastructure.repositories.models import Task as SQLAlchemyTask
from infrastructure.repositories.models import Category as SQLAlchemyCategory


class Converter[TD: DomainBase, TQ: SQLAlchemyBaseModel]:
    __converter_from_model = {
        DomainUser: SQLAlchemyUser,
        DomainTask: SQLAlchemyTask,
        DomainCategory: SQLAlchemyCategory,
    }

    @classmethod
    def convert_from_model_to_sqlalchemy(cls, model: TD) -> TQ:
        converted_model = cls.__converter_from_model.get(model.__class__)
        if converted_model is None:
            raise
        return converted_model(
            **{
                key: (
                    value.as_generic_type()
                    if isinstance(value, BaseValueObject)
                    else value
                )
                for key, value in model.__dict__.items()
                if key
                in {
                    prop.key
                    for prop in class_mapper(converted_model).iterate_properties
                    if isinstance(prop, sqlalchemy.orm.ColumnProperty)
                }
            }
        )
