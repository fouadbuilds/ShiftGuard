# Showcase Fixes Design

## Goal

Make ShiftGuard's final behaviour and onboarding match the project feedback before creating any showcase material.

## Scope

1. Create one review-only manager draft that covers every confirmed conflict.
2. Prove that behaviour with focused automated tests.
3. Add a clear README "Before you start" section.

## Behaviour

The deterministic conflict checker remains the source of truth. When one or more conflicts exist, the Groq boundary receives the complete sequence and produces one concise message to Dana. The message asks to discuss alternatives without claiming anything was sent, changed, or resolved. Telegram continues to label the output as a draft for Chloe's review.

No showcase screenshots, recording, LinkedIn post, or resume material are included in this change.

## Files

- `src/shiftguard/drafting.py`: accept and format all confirmed conflicts for one Groq prompt.
- `src/shiftguard/groq_drafting.py`: preserve the API boundary while accepting the conflict sequence.
- `src/shiftguard/telegram_draft.py`: pass the complete conflict list instead of only the first result.
- `tests/test_drafting.py`, `tests/test_groq_drafting.py`, `tests/test_telegram_draft.py`: cover the combined-draft path.
- `README.md`: add prerequisite information before setup steps.
