from pathlib import Path

from shiftguard.conflicts import find_conflicts
from shiftguard.schedule_data import load_schedule


def main() -> None:
    schedule_path = Path(__file__).parents[2] / "data" / "demo_schedule.json"
    schedule = load_schedule(schedule_path)
    conflicts = find_conflicts(
        shifts=schedule.shifts,
        protected_events=schedule.protected_events,
        buffer_minutes=30,
    )

    print(f"ShiftGuard found {len(conflicts)} conflict(s):")
    for conflict in conflicts:
        print(
            f"- {conflict.shift.title} conflicts with "
            f"{conflict.protected_event.title}"
        )
