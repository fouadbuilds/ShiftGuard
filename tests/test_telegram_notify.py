from shiftguard import telegram_notify
from shiftguard.telegram import TelegramSettings


def test_notification_command_sends_the_demo_conflicts(monkeypatch, capsys) -> None:
    settings = TelegramSettings(bot_token="test-token", chat_id="123456")
    sent: dict[str, object] = {}

    monkeypatch.setattr(
        telegram_notify.TelegramSettings,
        "from_environment",
        lambda: settings,
    )
    monkeypatch.setattr(
        telegram_notify,
        "send_telegram_message",
        lambda passed_settings, text: sent.update(
            settings=passed_settings,
            text=text,
        ),
    )

    telegram_notify.main()

    assert sent["settings"] == settings
    assert "ShiftGuard found 3 conflicts:" in sent["text"]
    assert "Telegram alert sent." in capsys.readouterr().out
