from shiftguard import telegram_draft
from shiftguard.groq_drafting import GroqSettings
from shiftguard.telegram import TelegramSettings


def test_draft_command_sends_a_review_only_draft_to_telegram(monkeypatch, capsys) -> None:
    groq_settings = GroqSettings(api_key="test-groq-key")
    telegram_settings = TelegramSettings(bot_token="test-token", chat_id="123456")
    sent: dict[str, object] = {}
    drafted_for: dict[str, object] = {}

    monkeypatch.setattr(
        telegram_draft.GroqSettings,
        "from_environment",
        lambda: groq_settings,
    )
    monkeypatch.setattr(
        telegram_draft.TelegramSettings,
        "from_environment",
        lambda: telegram_settings,
    )
    monkeypatch.setattr(
        telegram_draft,
        "create_manager_draft",
        lambda conflicts, api_key: drafted_for.update(
            conflicts=conflicts,
            api_key=api_key,
        )
        or "Hi Dana, could we discuss an alternative for my Friday shift? Thanks!",
    )
    monkeypatch.setattr(
        telegram_draft,
        "send_telegram_message",
        lambda settings, text: sent.update(settings=settings, text=text),
    )

    telegram_draft.main()

    assert drafted_for["api_key"] == "test-groq-key"
    conflict_titles = [conflict.shift.title for conflict in drafted_for["conflicts"]]
    assert conflict_titles == [
        "Harbour Foods shift - Friday",
        "Harbour Foods shift - Friday",
        "Harbour Foods shift - Saturday",
    ]
    assert sent["settings"] == telegram_settings
    assert sent["text"] == (
        "DRAFT FOR REVIEW (not sent to Dana):\n\n"
        "Hi Dana, could we discuss an alternative for my Friday shift? Thanks!"
    )
    assert "Telegram draft sent." in capsys.readouterr().out
