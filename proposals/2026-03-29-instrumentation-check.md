# Proposal: improve-forge should check for built-in instrumentation

## Learning
Apps with built-in chain logging find bugs faster than apps relying on external tests. The absence of instrumentation is a reliability gap.

## Source
eidos-assistant debug session (2026-03-29). 10 CI tests passed but the app failed on first real mic use. Chain logging (added later) found the bug in one line.

## Proposed Change
- **Target forge:** improve-forge
- **Target file:** `.claude/skills/improve.md` Step 2
- **Change:** Add "For software: check for built-in logging/instrumentation — if absent, that's a reliability gap" to Step 2 (Understand What Actually Exists)

## Why This Matters
Every future `/improve` run on any software project will check whether the app can tell you where it fails. This is the difference between "it doesn't work" and "it fails at step 3 because X."

## Evidence
eidos-assistant had 10 passing CI tests and zero instrumentation. Adding ChainLogger.swift with logging at every chain step (PTT → record → bucket → whisper → classify) immediately revealed: `ModuleNotFoundError: No module named 'faster_whisper'` — the Python path wasn't inherited from the shell in .app bundles.
