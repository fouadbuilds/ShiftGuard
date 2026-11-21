from datetime import datetime

from shiftguard.conflicts import Conflict, ScheduleEvent, find_conflicts


def test_returns_every_swim_event_that_conflicts_with_a_work_shift() -> None:
    shift = ScheduleEvent(
        title="Harbour Foods shift",
        starts_at=datetime(2026, 10, 23, 16, 0),
        ends_at=datetime(2026, 10, 23, 22, 0),
    )
    team_bus = ScheduleEvent(
        title="Team bus to Saint John",
        starts_at=datetime(2026, 10, 23, 14, 0),
        ends_at=datetime(2026, 10, 23, 18, 0),
    )
    taper_practice = ScheduleEvent(
        title="Swim practice (taper)",
        starts_at=datetime(2026, 10, 23, 17, 30),
        ends_at=datetime(2026, 10, 23, 19, 0),
    )
    unrelated_practice = ScheduleEvent(
        title="Swim practice",
        starts_at=datetime(2026, 10, 24, 6, 0),
        ends_at=datetime(2026, 10, 24, 7, 0),
    )

    conflicts = find_conflicts(
        shifts=[shift],
        protected_events=[team_bus, taper_practice, unrelated_practice],
        buffer_minutes=30,
    )

    assert conflicts == [
        Conflict(shift=shift, protected_event=team_bus),
        Conflict(shift=shift, protected_event=taper_practice),
    ]
