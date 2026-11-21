from datetime import datetime
from types import SimpleNamespace

from shiftguard.conflicts import Conflict, ScheduleEvent
from shiftguard.groq_drafting import create_manager_draft


def test_create_manager_draft_uses_the_groq_client_with_the_configured_key() -> None:
    conflict = Conflict(
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
        conflict,
        api_key="test-key",
        client_factory=FakeGroq,
    )

    assert draft == "Hi Dana, could we discuss an alternative for my Friday shift? Thanks!"
    assert captured["api_key"] == "test-key"
    assert captured["model"] == "openai/gpt-oss-20b"
