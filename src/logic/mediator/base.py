from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Iterable, Type

from domain.events.base import BaseEvent
from logic.commands.base import BaseCommand, CommandHandler
from logic.events.base import EventHandler
from logic.exceptions.mediator import (
    EventHandlersNotRegisteredException,
    CommandHandlersNotRegisteredException,
)


@dataclass
class Mediator[ET: BaseEvent, ER: Any, CT: BaseCommand, CR: Any]:
    events_map: dict[ET, list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )
    commands_map: dict[CT, list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )

    def register_event(self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]):
        self.events_map[event].extend(event_handlers)

    def register_command(
        self, command: CT, command_handlers: Iterable[CommandHandler[CT, CR]]
    ):
        self.commands_map[command].extend(command_handlers)

    async def publish(self, events: Iterable[ET]) -> Iterable[ER]:
        handlers = self.events_map.get(events[0].__class__)
        if not handlers:
            raise EventHandlersNotRegisteredException(events[0].__class__)
        result = []
        for event in events:
            handlers: Iterable[EventHandler] = self.events_map[event.__class__]
            result.extend([await handler.handle(event) for handler in handlers])
        return result

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = command.__class__
        handlers: list[CommandHandler] = self.commands_map.get(command_type)
        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type)
        return [await handler.handle(command=command) for handler in handlers]
