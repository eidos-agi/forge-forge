# Proposal: Formalize the proposals/ pattern in forge-forge

## Learning
learning-forge needs a governed way to propose improvements to other forges. Direct editing violates forge-forge's authority. The proposals/ directory pattern works: learning-forge writes proposals, forge-forge reviews them.

## Source
eidos-assistant session (2026-03-29). First attempt at learning-forge had it editing other forges' skill files directly. This was wrong — forge-forge is the overseer. Corrected to use proposals/ pattern.

## Proposed Change
- **Target forge:** forge-forge
- **Target file:** New skill: `forge-review-proposals.md`
- **Change:** Add a skill that reviews pending proposals in `proposals/`, accepts/rejects each, and applies accepted ones to target forges. Also add `proposals/` to the forge standard — any forge can receive proposals, but only forge-forge can approve them.

## Why This Matters
This closes the learning loop. Sessions produce learnings → learning-forge captures them → proposals land in forge-forge → forge-forge reviews and applies. Without the review step, proposals accumulate and rot. With it, the forge ecosystem improves with every session.

## Evidence
This session produced 4 proposals before this one. They're sitting in forge-forge/proposals/ with no mechanism to review or apply them. The pattern exists but the skill to process it doesn't.
