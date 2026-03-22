---
id: '0006'
title: Proposed manifest schema v1 — modular sections mapped to forge owners
status: open
evidence: MODERATE
sources: 1
created: '2026-03-22'
---

## Claim

The manifest should be organized by the forge that enforces each section, not by technical domain. This creates clear ownership and avoids one forge needing to understand everything. Proposed sections:

**repo** (forge-forge enforces): visibility, topics, branch_protection, org
**packaging** (ship-forge enforces): build_system, pypi.trusted_publisher, pypi.name, entry_points, readme.absolute_images
**quality** (foss-forge + ship-forge enforce): required_files[], min_grade.foss_check, min_grade.ship_check, min_grade.sec_audit
**security** (security-forge enforces): secret_scanning, dependency_audit, security_md_required
**deployment** (ship-forge enforces): platform (railway/none), health_check_path, env_vars_documented, graceful_shutdown
**dependencies** (ship-forge enforces): max_count, banned[], heavy_warning[]
**ci** (ship-forge enforces): workflows.ci, workflows.publish, permissions.contents_read, pre_commit_required
**exceptions** (any forge can read): array of {rule, justification, owner, expires}

Each section is optional. Missing section = use centralized default from forge-forge. Present section = override.

## Supporting Evidence

> **Evidence: [MODERATE]** — Synthesis of GPT-5.2 recommendations, Gemini SRE patterns, and session experience with forge ownership, retrieved 2026-03-22

## Caveats

None identified yet.
