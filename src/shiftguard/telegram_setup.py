import os
from pathlib import Path

from dotenv import load_dotenv

from shiftguard.telegram import discover_chat_id


def main() -> None:
    project_root = Path(__file__).parents[2]
    load_dotenv(project_root / ".env", override=False)
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")

    if not bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured")

    chat_id = discover_chat_id(bot_token)
    print(f"TELEGRAM_CHAT_ID={chat_id}")
