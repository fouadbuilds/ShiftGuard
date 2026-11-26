"""Send a review-only Groq draft to Chloe's private Telegram chat."""

from pathlib import Path

from shiftguard.conflicts import find_conflicts
from shiftguard.groq_drafting import GroqSettings, create_manager_draft
from shiftguard.schedule_data import load_schedule
from shiftguard.telegram import TelegramSettings, send_telegram_message


def main() -> None:
    groq_settings = GroqSettings.from_environment()
    telegram_settings = TelegramSettings.from_environment()
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

    draft = create_manager_draft(
        conflicts,
        api_key=groq_settings.api_key,
    )
    message = f"DRAFT FOR REVIEW (not sent to Dana):\n\n{draft}"
    send_telegram_message(telegram_settings, message)
    print("Telegram draft sent.")
