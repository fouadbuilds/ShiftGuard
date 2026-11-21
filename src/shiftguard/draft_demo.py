"""Print an AI-generated message draft for the first demo conflict."""

import sys
from pathlib import Path
from typing import Any

from shiftguard.conflicts import find_conflicts
from shiftguard.groq_drafting import GroqSettings, create_manager_draft
from shiftguard.schedule_data import load_schedule


def main() -> None:
    configure_utf8_output(sys.stdout)
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


def configure_utf8_output(output: Any) -> None:
    """Use UTF-8 when supported so model-generated text prints on Windows."""
    reconfigure = getattr(output, "reconfigure", None)
    if reconfigure is not None:
        reconfigure(encoding="utf-8")
