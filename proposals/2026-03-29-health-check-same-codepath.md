# Proposal: improve-forge should verify health checks test the real code path

## Learning
Health checks that use a different code path than the real operation give false confidence. The health check said "Whisper OK" while the real transcription failed.

## Source
eidos-assistant debug session (2026-03-29). Health check ran `python3 -c 'from faster_whisper import WhisperModel'` via `/bin/zsh -l` (login shell, full PATH). Real transcription ran Python via `Process()` from a .app bundle (no login shell, no PATH). Health check passed. Real operation failed.

## Proposed Change
- **Target forge:** improve-forge
- **Target file:** `.claude/skills/improve.md` Step 3 (Score) reliability dimension
- **Change:** When scoring reliability, specifically check: "Do health checks/smoke tests use the same code path as real operations? If health checks pass but the real path is untested, reliability score should reflect that gap."

## Why This Matters
False-positive health checks are worse than no health checks — they create confidence that masks real failures. Every future `/improve` run should catch this pattern.

## Evidence
```
[11:24:48.607] [OK] Whisper (faster-whisper)     ← health check (login shell)
[11:26:50.465] [FAIL] CHAIN FAILED — No module named 'faster_whisper'  ← real path (.app process)
```
