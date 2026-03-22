---
id: '0005'
title: >-
  Key pitfalls: scope creep, non-idempotent enforcement, exception rot, blast
  radius
status: open
evidence: HIGH
sources: 1
created: '2026-03-22'
---

## Claim

Top failure modes: (1) Scope creep — manifest tries to cover everything, becomes unmaintainable. Mitigation: modular sections, schema versioning. (2) Non-idempotent enforcement — agents re-run and create churn (formatting diffs, ordering changes). Mitigation: canonicalization, stable sorting, separate computed vs declared fields. (3) Exception rot — every repo becomes special over time. Mitigation: exceptions require justification + owner + expiry date. (4) Blast radius — bot that can change visibility/branch protection is dangerous. Mitigation: split read-only detection from privileged apply, require human approval for high-risk changes.

## Supporting Evidence

> **Evidence: [HIGH]** — GPT-5.2 analysis of common failure modes in policy-as-code systems, retrieved 2026-03-22

## Caveats

None identified yet.
