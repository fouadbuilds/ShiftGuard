from datetime import datetime

from shiftguard.conflicts import ScheduleEvent, shift_conflicts_with_event


def test_detects_a_shift_that_overlaps_the_team_bus() -> None:
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

    assert shift_conflicts_with_event(shift, team_bus) is True


def test_detects_a_shift_that_uses_the_team_bus_buffer() -> None:
    shift = ScheduleEvent(
        title="Harbour Foods shift",
        starts_at=datetime(2026, 10, 23, 16, 0),
        ends_at=datetime(2026, 10, 23, 18, 0),
    )
    team_bus = ScheduleEvent(
        title="Team bus to Saint John",
        starts_at=datetime(2026, 10, 23, 18, 15),
        ends_at=datetime(2026, 10, 23, 22, 0),
    )

    assert shift_conflicts_with_event(shift, team_bus, buffer_minutes=30) is True
