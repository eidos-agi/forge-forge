---
id: "GUARD-001"
type: "guardrail"
title: "No software — skills and templates only"
status: "active"
date: "2026-03-22"
---

## Rule
forge-forge must never become installable software. It is skills, templates, and a registry file. Nothing more.

## Why
Consistency across the forge ecosystem. The forge pattern is defined by this constraint.

## Violation Examples
- Adding pyproject.toml with a build system
- Writing a CLI tool
- Publishing to any package registry
