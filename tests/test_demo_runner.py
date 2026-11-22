from shiftguard import demo


def test_demo_command_sends_alert_before_review_draft(monkeypatch, capsys) -> None:
    steps: list[str] = []

    monkeypatch.setattr(demo, "send_conflict_alert", lambda: steps.append("alert"))
    monkeypatch.setattr(demo, "send_review_draft", lambda: steps.append("draft"))

    demo.main()

    assert steps == ["alert", "draft"]
    output = capsys.readouterr().out
    assert "Running ShiftGuard demo..." in output
    assert "ShiftGuard demo complete." in output
