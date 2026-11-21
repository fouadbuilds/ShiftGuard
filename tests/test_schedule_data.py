import json
from datetime import datetime
from pathlib import Path

from shiftguard.conflicts import ScheduleEvent, find_conflicts
from shiftguard.schedule_data import load_schedule


def test_loads_shifts_and_protected_events_from_json(tmp_path: Path) -> None:
    schedule_path = tmp_path / "schedule.json"
    schedule_path.write_text(
        json.dumps(
            {
                "shifts": [
                    {
                        "title": "Harbour Foods shift",
                        "starts_at": "2026-10-23T16:00:00",
                        "ends_at": "2026-10-23T22:00:00",
                    }
                ],
                "protected_events": [
                    {
                        "title": "Team bus to Saint John",
                        "starts_at": "2026-10-23T14:00:00",
                        "ends_at": "2026-10-23T18:00:00",
                    }
                ],
            }
        )
    )

    schedule = load_schedule(schedule_path)

    assert schedule.shifts == [
        ScheduleEvent(
            title="Harbour Foods shift",
            starts_at=datetime(2026, 10, 23, 16, 0),
            ends_at=datetime(2026, 10, 23, 22, 0),
        )
    ]
    assert schedule.protected_events == [
        ScheduleEvent(
            title="Team bus to Saint John",
            starts_at=datetime(2026, 10, 23, 14, 0),
            ends_at=datetime(2026, 10, 23, 18, 0),
        )
    ]


def test_demo_schedule_finds_chloes_work_and_swim_conflicts() -> None:
    schedule = load_schedule(Path("data/demo_schedule.json"))

    conflicts = find_conflicts(
        shifts=schedule.shifts,
        protected_events=schedule.protected_events,
        buffer_minutes=30,
    )

    assert [
        (conflict.shift.title, conflict.protected_event.title)
        for conflict in conflicts
    ] == [
        ("Harbour Foods shift - Friday", "Team bus to Saint John"),
        ("Harbour Foods shift - Friday", "Swim practice (taper)"),
        ("Harbour Foods shift - Saturday", "Fundy Invitational"),
    ]
