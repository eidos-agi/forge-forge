# Proposal: improve-forge rubric should score language boundaries

## Learning
In multi-language apps (Swift+Python, JS+Rust, etc.), bugs concentrate at the language boundary — the handoff between runtimes. This deserves explicit attention in the reliability score.

## Source
eidos-assistant debug session (2026-03-29). Swift app shells out to Python for Whisper transcription. The Swift side worked. The Python side worked. The handoff (Process environment, PATH resolution, argument passing) is where it broke.

## Proposed Change
- **Target forge:** improve-forge
- **Target file:** `.claude/skills/improve.md` Step 2 + `templates/rubric.md`
- **Change:** Add to Step 2: "For multi-language apps: specifically check the language boundaries — that's where bugs hide." Add to rubric under Reliability: "Multi-language apps: are the runtime boundaries tested? Do shelled-out processes get the right environment?"

## Why This Matters
Multi-language apps are increasingly common (Swift+Python for ML, JS+Rust for performance, etc.). The language boundary is a blind spot that linters, type checkers, and single-language tests all miss.

## Evidence
Swift called `/bin/zsh -l -c python3 transcribe.py`. In Terminal: works. From .app: fails. The boundary was untested by every test in the suite.
