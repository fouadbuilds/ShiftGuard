from shiftguard import draft_demo
from shiftguard.groq_drafting import GroqSettings


def test_configure_utf8_output_uses_utf8_when_the_output_supports_it() -> None:
    calls: list[dict[str, str]] = []

    class FakeOutput:
        def reconfigure(self, **kwargs: str) -> None:
            calls.append(kwargs)

    draft_demo.configure_utf8_output(FakeOutput())

    assert calls == [{"encoding": "utf-8"}]


def test_draft_command_prints_a_reviewable_first_conflict_draft(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        draft_demo.GroqSettings,
        "from_environment",
        lambda: GroqSettings(api_key="test-key"),
    )
    monkeypatch.setattr(
        draft_demo,
        "create_manager_draft",
        lambda conflict, api_key: "Hi Dana, could we discuss an alternative for my Friday shift? Thanks!",
    )

    draft_demo.main()

    output = capsys.readouterr().out
    assert "Draft for Chloe to review before sending:" in output
    assert "Hi Dana, could we discuss an alternative" in output
