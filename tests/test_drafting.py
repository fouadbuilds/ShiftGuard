from datetime import datetime
from types import SimpleNamespace

from shiftguard.conflicts import Conflict, ScheduleEvent
from shiftguard.drafting import draft_manager_message


def test_drafts_a_manager_message_from_confirmed_conflict_facts() -> None:
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
                    message=SimpleNamespace(
                        content="Hi Dana, I have a team bus conflict with my Friday shift. Could we discuss a swap? Thanks!"
                    )
                )
            ]
        )

    draft = draft_manager_message(conflict, create_completion=create_completion)

    assert draft == "Hi Dana, I have a team bus conflict with my Friday shift. Could we discuss a swap? Thanks!"
    assert captured["model"] == "openai/gpt-oss-20b"
    assert captured["max_completion_tokens"] == 120
    assert "Harbour Foods shift - Friday" in captured["messages"][1]["content"]
    assert "Team bus to Saint John" in captured["messages"][1]["content"]
