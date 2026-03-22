---
id: '0003'
title: Terraform plan/apply model fits perfectly for agent-driven enforcement
status: open
evidence: HIGH
sources: 1
created: '2026-03-22'
---

## Claim

The enforcement model should follow Terraform's three-phase approach: (1) Desired state = manifest, (2) Observed state = what GitHub/PyPI/repo actually looks like right now, (3) Plan = diff between desired and observed, shown to user. Optional Apply = auto-remediate or open PR. This model is idempotent, safe for agents to run repeatedly, and gives humans the review step. Gemini specifically recommended separating read-only drift detection from privileged remediation to limit blast radius.

## Supporting Evidence

> **Evidence: [HIGH]** — GPT-5.2 (Terraform model recommendation) + Gemini 2.5 Pro (privilege separation), retrieved 2026-03-22

## Caveats

None identified yet.
