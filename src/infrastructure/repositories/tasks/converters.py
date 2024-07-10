from typing import Mapping, Any

from domain.models.task import Task
from domain.values.task_name import TaskName


def convert_sqlalchemy_task_to_model(task_model: Mapping[str, Any]) -> Task:
    return Task(
        oid=task_model.oid,
        user_oid=task_model.user_oid,
        category_oid=task_model.category_oid,
        name=TaskName(task_model.name),
        is_complete=task_model.is_complete,
        deadline=task_model.deadline,
        valid=False,
    )
