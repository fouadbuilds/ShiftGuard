"""Create reviewable manager-message drafts from confirmed schedule conflicts."""

from collections.abc import Callable
from typing import Any

from shiftguard.conflicts import Conflict


MODEL = "openai/gpt-oss-20b"
MAX_DRAFT_CHARACTERS = 500


def draft_manager_message(
    conflict: Conflict, *, create_completion: Callable[..., Any]
) -> str:
    """Return a concise draft for Chloe to review before she sends anything.

    ``create_completion`` is injected so this behaviour can be tested without
    calling an AI service. The caller owns the client, credentials, and any
    network request.
    """
    response = create_completion(
        model=MODEL,
        max_completion_tokens=120,
        messages=[
            {
                "role": "system",
                "content": (
                    "Write one concise, polite message from Chloe to her manager Dana. "
                    "Use only the supplied facts. Ask to discuss an alternative shift. "
                    "Return only the message body, under 75 words. Do not claim that "
                    "a message was sent, a shift was changed, or a replacement was found."
                ),
            },
            {
                "role": "user",
                "content": _conflict_facts(conflict),
            },
        ],
    )

    try:
        content = response.choices[0].message.content
    except (AttributeError, IndexError, TypeError) as error:
        raise RuntimeError("The drafting service returned an unexpected response") from error

    if not isinstance(content, str):
        raise RuntimeError("The drafting service did not return text")

    draft = content.strip()
    if not draft:
        raise RuntimeError("The drafting service returned an empty draft")
    if len(draft) > MAX_DRAFT_CHARACTERS:
        raise RuntimeError("The drafting service returned a draft that is too long")

    return draft


def _conflict_facts(conflict: Conflict) -> str:
    """Format the deterministic conflict data as plain facts for the model."""
    return (
        "Confirmed schedule conflict:\n"
        f"- Work shift: {conflict.shift.title}\n"
        f"- Shift time: {conflict.shift.starts_at:%A, %B %d, %I:%M %p} "
        f"to {conflict.shift.ends_at:%I:%M %p}\n"
        f"- Protected commitment: {conflict.protected_event.title}\n"
        f"- Commitment time: {conflict.protected_event.starts_at:%A, %B %d, %I:%M %p} "
        f"to {conflict.protected_event.ends_at:%I:%M %p}"
    )
