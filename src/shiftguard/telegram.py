import json
import os
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

from shiftguard.conflicts import Conflict


@dataclass(frozen=True)
class TelegramSettings:
    bot_token: str
    chat_id: str

    @classmethod
    def from_environment(
        cls,
        env_path: Path | None = None,
    ) -> "TelegramSettings":
        if env_path is None:
            env_path = Path(__file__).parents[2] / ".env"

        load_dotenv(dotenv_path=env_path, override=False)
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")

        if not bot_token or not chat_id:
            raise RuntimeError("Telegram settings are not configured")

        return cls(bot_token=bot_token, chat_id=chat_id)


def format_conflict_alert(conflicts: list[Conflict]) -> str:
    count = len(conflicts)
    label = "conflict" if count == 1 else "conflicts"
    lines = [f"\u26a0\ufe0f ShiftGuard found {count} {label}:", ""]

    for conflict in conflicts:
        lines.append(
            f"- {conflict.shift.title} overlaps "
            f"{conflict.protected_event.title}."
        )

    return "\n".join(lines)


def send_telegram_message(
    settings: TelegramSettings,
    text: str,
    opener=urlopen,
) -> None:
    request = Request(
        url=f"https://api.telegram.org/bot{settings.bot_token}/sendMessage",
        data=json.dumps({"chat_id": settings.chat_id, "text": text}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with opener(request, timeout=10) as response:
            payload = json.loads(response.read())
    except (HTTPError, URLError, TimeoutError):
        raise RuntimeError("Could not send Telegram alert") from None

    if not payload.get("ok"):
        raise RuntimeError("Telegram rejected the alert")


def discover_chat_id(bot_token: str, opener=urlopen) -> str:
    request = Request(
        url=f"https://api.telegram.org/bot{bot_token}/getUpdates",
        method="GET",
    )

    try:
        with opener(request, timeout=10) as response:
            payload = json.loads(response.read())
    except (HTTPError, URLError, TimeoutError):
        raise RuntimeError("Could not read Telegram updates") from None

    if not payload.get("ok"):
        raise RuntimeError("Telegram rejected the setup request")

    for update in reversed(payload.get("result", [])):
        chat = update.get("message", {}).get("chat", {})
        if chat.get("type") == "private" and "id" in chat:
            return str(chat["id"])

    raise RuntimeError("No private chat was found; send /start to the bot first")
