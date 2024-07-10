import dataclasses

from domain.events.users import NewUserCreated, UserDeleted
from domain.events.categories import NewCategoryCreated, CategoryDeleted
from domain.events.tasks import NewTaskCreated, TaskDeleted
from domain.models.category import Category
from domain.models.task import Task
from domain.values.email import Email
from domain.values.password import Password, HashedPassword
from domain.models.base import Base


@dataclasses.dataclass
class User(Base):
    email: Email
    password: Password | HashedPassword
    categories: set[Category] = dataclasses.field(
        default_factory=set[Category], kw_only=True
    )
    tasks: set[Task] = dataclasses.field(default_factory=set[Task], kw_only=True)
    is_deleted: bool = dataclasses.field(default=False, kw_only=True)

    @classmethod
    def create_user(cls, email: Email, password: Password) -> "User":
        new_user = cls(email=email, password=password)
        new_user.register_event(
            NewUserCreated(
                email=email.as_generic_type(), password=password.as_generic_type()
            )
        )
        return new_user

    def delete_user(self) -> None:
        self.is_deleted = True
        self.register_event(UserDeleted(self.oid))

    def create_new_category(self, category: Category) -> None:
        self.register_event(
            NewCategoryCreated(
                user_oid=self.oid, title=category.title.as_generic_type()
            )
        )
        self.categories.add(category)

    def create_new_task(self, task: Task) -> None:
        self.register_event(
            NewTaskCreated(
                user_oid=self.oid,
                name=task.name.as_generic_type(),
                category_oid=task.category_oid,
                is_complete=task.is_complete,
                deadline=task.deadline,
            )
        )
        self.tasks.add(task)

    def delete_task(self, task: Task) -> None:
        self.register_event(TaskDeleted(task.oid))
        self.tasks.remove(task)

    def delete_category(self, category: Category) -> None:
        self.register_event(CategoryDeleted(category.oid))
        self.categories.remove(category)
