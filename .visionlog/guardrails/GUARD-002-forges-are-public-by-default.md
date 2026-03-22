---
id: "GUARD-002"
type: "guardrail"
title: "Forges are public by default"
status: "active"
date: "2026-03-22"
---

## Rule
All forges created via `/forge-init` must be public GitHub repos under `eidos-agi/`. No private forges.

## Why
Forges are knowledge, not proprietary code. Making them public enables the community to use, fork, and contribute. It also forces quality — if it's public, it has to be good.

## Violation Examples
- Creating a private forge repo
- Creating a forge outside the eidos-agi org
