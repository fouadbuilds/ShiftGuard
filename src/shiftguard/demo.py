"""Run ShiftGuard's alert and review-draft demo in a safe order."""

from shiftguard.telegram_draft import main as send_review_draft
from shiftguard.telegram_notify import main as send_conflict_alert


def main() -> None:
    print("Running ShiftGuard demo...")
    send_conflict_alert()
    send_review_draft()
    print("ShiftGuard demo complete.")
