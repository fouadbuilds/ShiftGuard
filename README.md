# ShiftGuard

ShiftGuard is a small AI-assisted safety net for **Chloe Nguyen**, a student swimmer who also works part-time shifts. It spots a work shift that clashes with a swim commitment, including travel time, then sends Chloe a Telegram alert and a manager-message draft for her to review.

- ShiftGuard helps Chloe notice a problem early. Chloe stays in control of every decision and every message.

## The problem

Chloe's busy schedule has two separate sources of commitments: work shifts and swim-team events. A shift can look valid on paper but still be impossible in practice—for example, a 6:00 PM finish before a 6:15 PM team bus. That 15-minute gap is not enough time to travel or warm up.

The demo applies a **30-minute buffer before every protected swim commitment**. It therefore catches both direct overlaps and practical travel-time conflicts.

## What it does

1. Loads fictional work shifts and swim commitments from `data/demo_schedule.json`.
2. Finds every work shift that overlaps a protected commitment or its 30-minute lead-in buffer.
3. Sends Chloe a Telegram alert listing the conflicts.
4. Uses Groq's `openai/gpt-oss-20b` model to draft one short, polite message to Dana that covers every detected conflict.
5. Sends that draft to Chloe's private Telegram chat with a clear review-only label.

## What it does not do

- Send a message to Dana or any manager.
- Change, cancel, or accept work shifts.
- Find a replacement worker.
- Invent schedule facts that were not supplied.
- Treat an AI draft as an approved action.

## Architecture

```text
demo schedule JSON
        |
        v
conflict checker -- 30-minute buffer --> Telegram conflict alert
        |
        v
confirmed conflict facts --> Groq draft generator --> review-only Telegram draft
```

The deterministic code decides whether a conflict exists. The language model only turns already-confirmed facts into a human-readable draft. This separation keeps the important scheduling decision predictable and testable.

## Before you start

You will need:

- Python 3.11 or newer.
- [uv](https://docs.astral.sh/uv/) to install and run the project.
- A Telegram account and a bot token from [BotFather](https://t.me/BotFather).
- A private Telegram chat ID for the account that will receive alerts. Send `/start` to your bot before discovering it.
- A [Groq API key](https://console.groq.com/keys) for the review-only message draft.

Keep the token and API key private. They belong only in your local `.env` file, which Git ignores.

## Setup

### 1. Install dependencies


```bash
pip install uv
```

```bash
uv sync
```


Fill in the values in `.env`:

```env
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-private-chat-id
GROQ_API_KEY=your-groq-api-key
```


To discover the private Telegram chat ID after sending `/start` to your bot:

```bash
uv run shiftguard-telegram-setup
```

Copy the printed chat ID into `.env` as `TELEGRAM_CHAT_ID`.

## Demo

Run the two commands below in order:

```bash
uv run shiftguard-send-demo-alert
uv run shiftguard-send-demo-draft
```

Or use the one-command presentation flow:

```bash
uv run shiftguard-demo
```

Expected result in Telegram:

1. A conflict alert that identifies the detected scheduling problems.
2. A second message labelled `DRAFT FOR REVIEW (not sent to Dana)` containing a suggested message Chloe can copy, edit, or ignore.

To view the draft in the terminal instead of sending it to Telegram:

```bash
uv run shiftguard-draft-demo-message
```

## Testing

```bash
uv run pytest
```

The test suite covers the buffer-aware conflict rule, schedule loading, Telegram formatting and delivery boundaries, Groq draft configuration, and the review-only Telegram draft flow.

