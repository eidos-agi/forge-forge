# Proposal: improve-forge should check skill pipelines in forges

## Learning
Forges have skills that depend on each other's output. If skill A's output is optional but skill B requires it as input, the pipeline is broken. This is a production readiness bug specific to knowledge forges.

## Source
brutal-forge improvement run (2026-03-29). `/brutalize` offered to save the report as an optional step. `/shame-board` required saved reports to function. The pipeline between skills was broken because saving was optional.

## Proposed Change
- **Target forge:** improve-forge
- **Target file:** `.claude/skills/improve.md` Step 2 + Step 6
- **Change:** For knowledge forges, add: "Trace the pipeline between skills. Does one skill's output feed another's input? Is any link in that chain optional when it should be mandatory?" This is the forge equivalent of integration testing.

## Why This Matters
As the forge ecosystem grows (25+ forges), skill pipelines become more complex. A forge with 4 skills that don't connect is 4 isolated tools, not a system. Checking the pipeline is how improve-forge evaluates forge coherence.

## Evidence
brutal-forge: `/brutalize` Step 5 said "Save report?" (optional). `/shame-board` Step 1 said "Find all reports" (required). Fix: made saving mandatory in brutalize.
