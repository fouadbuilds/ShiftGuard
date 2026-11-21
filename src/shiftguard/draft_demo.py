"""Print an AI-generated message draft for the first demo conflict."""

from pathlib import Path

from shiftguard.conflicts import find_conflicts
from shiftguard.groq_drafting import GroqSettings, create_manager_draft
from shiftguard.schedule_data import load_schedule


def main() -> None:
    settings = GroqSettings.from_environment()
    schedule_path = Path(__file__).parents[2] / "data" / "demo_schedule.json"
    schedule = load_schedule(schedule_path)
    conflicts = find_conflicts(
        shifts=schedule.shifts,
        protected_events=schedule.protected_events,
        buffer_minutes=30,
    )

    if not conflicts:
        print("No conflicts found, so there is no message to draft.")
        return

    draft = create_manager_draft(conflicts[0], api_key=settings.api_key)
    print("Draft for Chloe to review before sending:\n")
    print(draft)
