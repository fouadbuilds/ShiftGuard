from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class ScheduleEvent:
    title: str
    starts_at: datetime
    ends_at: datetime


def shift_conflicts_with_event(
    shift: ScheduleEvent,
    protected_event: ScheduleEvent,
    buffer_minutes: int = 0,
) -> bool:
    protected_start = protected_event.starts_at - timedelta(minutes=buffer_minutes)

    return (
        shift.starts_at < protected_event.ends_at
        and protected_start < shift.ends_at
    )
