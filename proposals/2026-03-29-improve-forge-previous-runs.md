# Proposal: improve-forge Step 0 is validated — make it a forge standard

## Learning
Checking previous improvement runs before starting a new one prevents duplicate work and builds on prior findings. Step 0 (check previous runs) was added to improve-forge and immediately proved valuable — the second self-improvement run built on the first instead of repeating it.

## Source
improve-forge self-improvement run 2 (2026-03-29). Run 1 fixed packaging (3→6). Run 2 checked the snapshot from run 1, saw `next_priority: reliability`, and focused there instead of re-examining packaging.

## Proposed Change
- **Target forge:** forge-forge (forge standard)
- **Change:** Recommend that any forge that produces artifacts (reports, snapshots, scores) should check for prior artifacts before starting a new run. This is the "check previous work" pattern. Consider adding to the forge standard template.

## Why This Matters
As agents run forges repeatedly on the same projects, they need continuity. Without checking prior runs, each invocation starts from zero. With it, each run is incremental improvement.

## Evidence
improve-forge run 1: overall 35/70, fixed packaging. Run 2: read prior snapshot, skipped packaging, focused on production readiness and reliability. Overall 35→41 across two runs.
