# ShiftGuard demo script

This is a short, repeatable walkthrough for showing the project.

## Before you present

- Open your private ShiftGuard Telegram chat on screen.
- Open a terminal in the project folder.
- Confirm your local `.env` has the Telegram and Groq keys. Do not show the file or its values.

## What to say and do

### 1. Set the scene (15 seconds)

> Chloe is a student swimmer who also works part-time. A work shift can look available but still make her miss a team bus or swim commitment. ShiftGuard catches those practical conflicts early.

### 2. Explain the rule (15 seconds)

> The conflict decision is deterministic, not AI-generated. ShiftGuard adds a 30-minute buffer before protected swim events, so a shift that ends only 15 minutes before a bus is still flagged.

### 3. Run the demo (15 seconds)

```powershell
uv run shiftguard-demo
```

### 4. Show Telegram (20 seconds)

Point out the two messages:

1. The conflict alert lists every detected issue.
2. The draft is labelled `DRAFT FOR REVIEW (not sent to Dana)`.

> Groq only writes the wording from the confirmed facts. Chloe can copy, edit, or ignore it. The bot cannot contact Dana or change a shift.

### 5. Close (10 seconds)

> This keeps the high-stakes decision predictable while still removing the awkward work of writing a last-minute manager message.

## If someone asks

**Why use AI at all?**

The rule-based system finds the conflict reliably. AI is useful for turning that structured information into a polite, human-sounding draft.

**Could it accidentally message the manager?**

No. The configured Telegram chat belongs to Chloe, and the application has no manager contact details or shift-management permissions.

**What would you build next?**

Connect a real schedule source and flag a newly added meet before the work schedule is published, while keeping Chloe's approval step.
