from pathlib import Path

from shiftguard.conflicts import find_conflicts
from shiftguard.schedule_data import load_schedule
from shiftguard.telegram import (
    TelegramSettings,
    format_conflict_alert,
    send_telegram_message,
)


def main() -> None:
    settings = TelegramSettings.from_environment()
    schedule_path = Path(__file__).parents[2] / "data" / "demo_schedule.json"
    schedule = load_schedule(schedule_path)
    conflicts = find_conflicts(
        shifts=schedule.shifts,
        protected_events=schedule.protected_events,
        buffer_minutes=30,
    )
    alert = format_conflict_alert(conflicts)

    send_telegram_message(settings, alert)
    print("Telegram alert sent.")
