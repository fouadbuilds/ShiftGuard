import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from shiftguard.conflicts import ScheduleEvent


@dataclass(frozen=True)
class Schedule:
    shifts: list[ScheduleEvent]
    protected_events: list[ScheduleEvent]


def load_schedule(path: Path) -> Schedule:
    data = json.loads(path.read_text())

    return Schedule(
        shifts=[_to_event(event) for event in data["shifts"]],
        protected_events=[_to_event(event) for event in data["protected_events"]],
    )


def _to_event(data: dict[str, str]) -> ScheduleEvent:
    return ScheduleEvent(
        title=data["title"],
        starts_at=datetime.fromisoformat(data["starts_at"]),
        ends_at=datetime.fromisoformat(data["ends_at"]),
    )
