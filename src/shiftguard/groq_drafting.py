"""Configuration and API boundary for ShiftGuard's Groq-powered drafts."""

import os
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from groq import Groq

from shiftguard.conflicts import Conflict
from shiftguard.drafting import draft_manager_message


@dataclass(frozen=True)
class GroqSettings:
    api_key: str

    @classmethod
    def from_environment(cls, env_path: Path | None = None) -> "GroqSettings":
        """Load the API key from the local, git-ignored .env file."""
        if env_path is None:
            env_path = Path(__file__).parents[2] / ".env"

        load_dotenv(dotenv_path=env_path, override=False)
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not configured")

        return cls(api_key=api_key)


def create_manager_draft(
    conflicts: Sequence[Conflict],
    *,
    api_key: str,
    client_factory: Callable[..., Any] = Groq,
) -> str:
    """Ask Groq for one reviewable draft based on confirmed conflicts."""
    client = client_factory(api_key=api_key)
    return draft_manager_message(
        conflicts,
        create_completion=client.chat.completions.create,
    )
