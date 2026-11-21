from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class ScheduleEvent:
    title: str
    starts_at: datetime
    ends_at: datetime


@dataclass(frozen=True)
class Conflict:
    shift: ScheduleEvent
    protected_event: ScheduleEvent


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


def find_conflicts(
    shifts: list[ScheduleEvent],
    protected_events: list[ScheduleEvent],
    buffer_minutes: int = 0,
) -> list[Conflict]:
    conflicts: list[Conflict] = []

    for shift in shifts:
        for protected_event in protected_events:
            if shift_conflicts_with_event(shift, protected_event, buffer_minutes):
                conflicts.append(
                    Conflict(shift=shift, protected_event=protected_event)
                )

    return conflicts
