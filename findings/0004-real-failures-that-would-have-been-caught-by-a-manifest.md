---
id: '0004'
title: Real failures that would have been caught by a manifest
status: open
evidence: HIGH
sources: 1
created: '2026-03-22'
---

## Claim

Three real failures from this session would have been prevented: (1) visionlog repo set to private when it should be public — manifest would declare visibility: public, drift detection catches it. (2) railguey publish workflow missing contents:read — manifest would declare the exact workflow permissions needed. (3) railguey README with relative image URLs — manifest would declare readme.images: absolute. Also: claude-session-commons shipped to PyPI with no LICENSE, clawdflare had no LICENSE. A manifest declaring license: MIT with required_files including LICENSE would have blocked both.

## Supporting Evidence

> **Evidence: [HIGH]** — Direct observation from this session's work, retrieved 2026-03-22

## Caveats

None identified yet.
