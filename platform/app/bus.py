from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .store import Store, utcnow

EventCallback = Callable[[dict[str, Any]], None]


class EventBus:
    """Append-only trajectory with an optional progress callback."""

    def __init__(self, store: Store, on_event: EventCallback | None = None) -> None:
        self.store = store
        self.on_event = on_event

    async def emit(
        self,
        run_id: str,
        kind: str,
        service: str,
        payload: dict[str, Any] | None = None,
        stage: str | None = None,
    ) -> dict[str, Any]:
        event = {
            "run_id": run_id,
            "sequence": self.store.next_sequence(run_id),
            "timestamp": utcnow(),
            "kind": kind,
            "service": service,
            "stage": stage,
            "payload": payload or {},
        }
        self.store.append_event(event)
        if self.on_event:
            self.on_event(event)
        return event
