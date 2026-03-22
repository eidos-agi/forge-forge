---
id: '0002'
title: >-
  Hybrid model is the right architecture — centralized baseline + repo-local
  overrides
status: open
evidence: HIGH
sources: 1
created: '2026-03-22'
---

## Claim

Both GPT-5.2 and Gemini 2.5 Pro independently recommended a hybrid model: centralized baseline policy (in forge-forge) defining org-wide defaults + minimum standards, plus repo-local manifest (.forge/manifest.yaml) declaring repo-specific intent and controlled exceptions. Central-only loses repo autonomy and creates exception bloat. Local-only risks policy drift across dozens of repos. Hybrid mirrors how mature infra systems work (Terraform modules + per-env overrides, Kubernetes namespaces + cluster policies).

## Supporting Evidence

> **Evidence: [HIGH]** — GPT-5.2 + Gemini 2.5 Pro consensus, retrieved 2026-03-22

## Caveats

None identified yet.
