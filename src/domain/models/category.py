import dataclasses
import uuid

from domain.models.base import Base
from domain.models.task import Task
from domain.values.category_title import CategoryTitle
from domain.events.categories import CategoryUpdated


@dataclasses.dataclass
class Category(Base):
    user_oid: uuid.UUID
    title: CategoryTitle
    tasks: set[Task] | None = dataclasses.field(default=None)

    def update_category(self, new_title: CategoryTitle):
        self.register_event(
            CategoryUpdated(category_oid=self.oid, title=new_title.as_generic_type())
        )
        self.title = new_title

    def __hash__(self):
        return hash(self.oid)
