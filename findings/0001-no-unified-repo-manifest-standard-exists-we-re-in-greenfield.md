---
id: '0001'
title: No unified repo manifest standard exists — we're in greenfield
status: open
evidence: HIGH
sources: 1
created: '2026-03-22'
---

## Claim

Existing tools are fragmented by concern: probot/settings (GitHub settings), Terraform (infra), Renovate (deps), CODEOWNERS (review), OpenSSF Scorecard (security scoring), REUSE (licensing). Apache has .asf.yaml, CNCF uses Prow + OWNERS. Nobody has a single manifest covering forge settings + packaging + quality gates + agent-readiness. The closest is OpenSSF Allstar for security enforcement, but it only covers security posture, not packaging or quality.

## Supporting Evidence

> **Evidence: [HIGH]** — GPT-5.2 comprehensive analysis of existing tools + foundation practices (Apache, CNCF, Linux Foundation), retrieved 2026-03-22

## Caveats

None identified yet.
