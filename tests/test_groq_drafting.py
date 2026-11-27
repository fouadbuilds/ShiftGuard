from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

from shiftguard.conflicts import Conflict, ScheduleEvent
from shiftguard.groq_drafting import GroqSettings, create_manager_draft


def test_local_env_file_overrides_a_stale_groq_key_in_the_process(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setenv("GROQ_API_KEY", "old-key")
    env_path = tmp_path / ".env"
    env_path.write_text("GROQ_API_KEY=new-key\n")

    settings = GroqSettings.from_environment(env_path=env_path)

    assert settings == GroqSettings(api_key="new-key")


def test_create_manager_draft_forwards_every_conflict_to_the_groq_client() -> None:
    friday_conflict = Conflict(
        shift=ScheduleEvent(
            title="Harbour Foods shift - Friday",
            starts_at=datetime(2026, 10, 23, 16, 0),
            ends_at=datetime(2026, 10, 23, 22, 0),
        ),
        protected_event=ScheduleEvent(
            title="Team bus to Saint John",
            starts_at=datetime(2026, 10, 23, 14, 0),
            ends_at=datetime(2026, 10, 23, 18, 0),
        ),
    )
    saturday_conflict = Conflict(
        shift=ScheduleEvent(
            title="Harbour Foods shift - Saturday",
            starts_at=datetime(2026, 10, 24, 9, 0),
            ends_at=datetime(2026, 10, 24, 15, 0),
        ),
        protected_event=ScheduleEvent(
            title="Fundy Invitational",
            starts_at=datetime(2026, 10, 24, 7, 0),
            ends_at=datetime(2026, 10, 24, 17, 0),
        ),
    )
    captured: dict[str, object] = {}

    def create_completion(**kwargs):
        captured.update(kwargs)
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content="Hi Dana, could we discuss an alternative for my Friday shift? Thanks!")
                )
            ]
        )

    class FakeGroq:
        def __init__(self, *, api_key: str) -> None:
            captured["api_key"] = api_key
            self.chat = SimpleNamespace(
                completions=SimpleNamespace(create=create_completion)
            )

    draft = create_manager_draft(
        [friday_conflict, saturday_conflict],
        api_key="test-key",
        client_factory=FakeGroq,
    )

    assert draft == "Hi Dana, could we discuss an alternative for my Friday shift? Thanks!"
    assert captured["api_key"] == "test-key"
    assert captured["model"] == "openai/gpt-oss-20b"
    facts = captured["messages"][1]["content"]
    assert "Harbour Foods shift - Friday" in facts
    assert "Harbour Foods shift - Saturday" in facts
