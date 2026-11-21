import json
from datetime import datetime
from pathlib import Path

from shiftguard.conflicts import Conflict, ScheduleEvent
from shiftguard.telegram import (
    TelegramSettings,
    discover_chat_id,
    format_conflict_alert,
    send_telegram_message,
)


def test_reads_telegram_settings_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "123456")

    settings = TelegramSettings.from_environment()

    assert settings.bot_token == "test-token"
    assert settings.chat_id == "123456"


def test_reads_telegram_settings_from_a_local_env_file(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    env_path = tmp_path / ".env"
    env_path.write_text("TELEGRAM_BOT_TOKEN=test-token\nTELEGRAM_CHAT_ID=123456\n")

    settings = TelegramSettings.from_environment(env_path=env_path)

    assert settings == TelegramSettings(bot_token="test-token", chat_id="123456")


def test_formats_a_conflict_as_a_telegram_alert() -> None:
    shift = ScheduleEvent(
        title="Harbour Foods shift - Friday",
        starts_at=datetime(2026, 10, 23, 16, 0),
        ends_at=datetime(2026, 10, 23, 22, 0),
    )
    team_bus = ScheduleEvent(
        title="Team bus to Saint John",
        starts_at=datetime(2026, 10, 23, 14, 0),
        ends_at=datetime(2026, 10, 23, 18, 0),
    )

    alert = format_conflict_alert([Conflict(shift=shift, protected_event=team_bus)])

    assert alert == (
        "⚠️ ShiftGuard found 1 conflict:\n\n"
        "- Harbour Foods shift - Friday overlaps Team bus to Saint John."
    )


def test_sends_an_alert_to_the_configured_telegram_chat() -> None:
    settings = TelegramSettings(bot_token="test-token", chat_id="123456")
    captured: dict[str, object] = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback) -> None:
            return None

        def read(self) -> bytes:
            return b'{"ok": true}'

    def opener(request, timeout: int):
        captured["url"] = request.full_url
        captured["body"] = json.loads(request.data)
        captured["timeout"] = timeout
        return FakeResponse()

    send_telegram_message(settings, "Test alert", opener=opener)

    assert captured == {
        "url": "https://api.telegram.org/bottest-token/sendMessage",
        "body": {"chat_id": "123456", "text": "Test alert"},
        "timeout": 10,
    }


def test_discovers_the_latest_private_chat_id() -> None:
    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback) -> None:
            return None

        def read(self) -> bytes:
            return json.dumps(
                {
                    "ok": True,
                    "result": [
                        {"message": {"chat": {"id": -100, "type": "group"}}},
                        {"message": {"chat": {"id": 123456, "type": "private"}}},
                    ],
                }
            ).encode()

    def opener(request, timeout: int):
        assert request.full_url == "https://api.telegram.org/bottest-token/getUpdates"
        assert timeout == 10
        return FakeResponse()

    assert discover_chat_id("test-token", opener=opener) == "123456"
