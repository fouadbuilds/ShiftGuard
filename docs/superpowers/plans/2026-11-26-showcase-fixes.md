# Showcase Fixes Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make one review-only ShiftGuard draft cover all confirmed conflicts and clarify setup prerequisites.

**Architecture:** Keep conflict detection deterministic. Pass the complete ordered conflict list into the existing Groq drafting boundary, format all facts in one prompt, and send one Telegram draft. Documentation remains separate from runtime behaviour.

**Tech Stack:** Python 3.12, pytest, Groq SDK, python-telegram-bot HTTP API, uv.

---

### Task 1: Specify the combined-draft behaviour

**Files:**
- Modify: `tests/test_drafting.py`
- Modify: `tests/test_groq_drafting.py`
- Modify: `tests/test_telegram_draft.py`

- [ ] Add a failing unit test showing that two conflicts appear in the facts supplied to Groq.
- [ ] Run the focused drafting test and confirm it fails because the current function accepts one conflict.
- [ ] Add a failing Telegram-flow test showing the complete conflict list is passed to drafting.
- [ ] Run the focused Telegram-flow test and confirm it fails because the command selects `conflicts[0]`.

### Task 2: Implement one complete review-only draft

**Files:**
- Modify: `src/shiftguard/drafting.py`
- Modify: `src/shiftguard/groq_drafting.py`
- Modify: `src/shiftguard/telegram_draft.py`

- [ ] Change the drafting API to accept a sequence of confirmed conflicts.
- [ ] Format each conflict as supplied fact; retain the existing safety instructions and character limit.
- [ ] Pass the full result of `find_conflicts()` to the Groq boundary.
- [ ] Run the focused tests and confirm they pass.

### Task 3: Clarify setup requirements

**Files:**
- Modify: `README.md`

- [ ] Add a "Before you start" section above setup listing Python 3.12+, uv, a Telegram account/bot token/private chat ID, and a Groq API key.
- [ ] Keep secrets out of examples and retain the existing `.env` instructions.

### Task 4: Verify and save the change

**Files:**
- Modify: `docs/superpowers/plans/2026-11-26-showcase-fixes.md`

- [ ] Run `uv run pytest`.
- [ ] Review `git diff --check` and `git diff` for accidental secrets.
- [ ] Commit the tested change with `fix: include every conflict in review draft`.
