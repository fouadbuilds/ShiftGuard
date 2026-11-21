from shiftguard import telegram_setup


def test_setup_command_prints_a_chat_id_without_printing_the_token(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setattr(telegram_setup, "discover_chat_id", lambda token: "123456")

    telegram_setup.main()

    output = capsys.readouterr().out
    assert "TELEGRAM_CHAT_ID=123456" in output
    assert "test-token" not in output
