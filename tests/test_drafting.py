from datetime import datetime
from types import SimpleNamespace

from shiftguard.conflicts import Conflict, ScheduleEvent
from shiftguard.drafting import draft_manager_message


def test_drafts_one_message_from_every_confirmed_conflict() -> None:
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
                    message=SimpleNamespace(
                        content="Hi Dana, I have a team bus conflict with my Friday shift. Could we discuss a swap? Thanks!"
                    )
                )
            ]
        )

    draft = draft_manager_message(
        [friday_conflict, saturday_conflict],
        create_completion=create_completion,
    )

    assert draft == "Hi Dana, I have a team bus conflict with my Friday shift. Could we discuss a swap? Thanks!"
    assert captured["model"] == "openai/gpt-oss-20b"
    assert captured["reasoning_effort"] == "low"
    assert captured["max_completion_tokens"] == 256
    assert "Harbour Foods shift - Friday" in captured["messages"][1]["content"]
    assert "Team bus to Saint John" in captured["messages"][1]["content"]
    assert "Harbour Foods shift - Saturday" in captured["messages"][1]["content"]
    assert "Fundy Invitational" in captured["messages"][1]["content"]
