import dataclasses
import uuid
from typing import override

from domain.events.base import BaseEvent


@dataclasses.dataclass
class Base:
    oid: uuid.UUID = dataclasses.field(
        default_factory=lambda: uuid.uuid4(), kw_only=True
    )
    __events: list[BaseEvent] = dataclasses.field(default_factory=list, kw_only=True)

    @override
    def __hash__(self) -> int:
        return hash(self.oid)

    @override
    def __eq__(self, __value: "Base") -> bool:
        return self.oid == __value.oid

    @override
    def __ne__(self, __value: "Base") -> bool:
        return self.oid != __value.oid

    def register_event(self, event: BaseEvent) -> None:
        self.__events.append(event)

    def pull_events(self) -> list[BaseEvent]:
        registered_events = self.__events.copy()
        self.__events.clear()
        return registered_events
