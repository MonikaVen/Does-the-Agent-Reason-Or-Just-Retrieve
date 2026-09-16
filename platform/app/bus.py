from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Any

from .store import Store, utcnow


class EventBus:
    """Append-only trajectory plus in-process fan-out for SSE."""

    def __init__(self, store: Store) -> None:
        self.store = store
        self._subs: dict[str, list[asyncio.Queue]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def subscribe(self, run_id: str) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue()
        async with self._lock:
            self._subs[run_id].append(queue)
        return queue

    async def unsubscribe(self, run_id: str, queue: asyncio.Queue) -> None:
        async with self._lock:
            subs = self._subs.get(run_id, [])
            if queue in subs:
                subs.remove(queue)

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
        async with self._lock:
            for queue in list(self._subs.get(run_id, [])):
                await queue.put(event)
        return event
