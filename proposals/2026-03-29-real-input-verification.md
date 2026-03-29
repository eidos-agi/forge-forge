# Proposal: improve-forge Step 6 should require real-input testing

## Learning
Synthetic test inputs hide environment and integration bugs. The first real user test is worth more than all synthetic tests combined.

## Source
eidos-assistant debug session (2026-03-29). All tests used macOS `say` command to generate audio. These ran from Terminal which has full PATH. The real app running from /Applications didn't have PATH. Synthetic tests passed; real use failed.

## Proposed Change
- **Target forge:** improve-forge
- **Target file:** `.claude/skills/improve.md` Step 6 (Verify)
- **Change:** Add: "If possible, test with real input (not synthetic). Synthetic tests can hide environment, permission, and integration bugs that only manifest in real usage."

## Why This Matters
Every future `/improve` verification step will push agents toward real-input testing. Prevents the false confidence of green CI with broken real-world behavior.

## Evidence
10/10 CI tests passing. 0/1 real microphone tests passing. The gap was invisible until a human held Cmd+E.
