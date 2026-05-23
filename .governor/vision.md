---
title: "forge-forge — The Forge Pattern"
type: "vision"
date: "2026-03-22"
---

## North Star

forge-forge owns the **Forge Standard** — the meta-layer that defines what a forge IS, how to create one, how to validate one, and the canonical registry of all forges in the Eidos AGI ecosystem.

## What is a Forge?

A forge is a repo that packages reusable AI agent knowledge as Claude Code skills and templates. The key properties:

1. **No software.** No pyproject.toml, no CLI, no package. Pure knowledge.
2. **Skills are markdown.** Each skill is a `.md` file in `.claude/skills/` with a trigger, instructions, and rules.
3. **Templates are parameterized.** Files in `templates/` with `{{VARIABLE}}` substitution.
4. **Visionlog is mandatory.** Every forge has a vision, goals, and guardrails.
5. **Public by default.** Forges are open source under `eidos-agi/`.

## Why Forges Exist

The agentic software ecosystem needs reusable patterns, but traditional packaging (npm, pip) is wrong for knowledge. A skill file doesn't need versioning, dependency resolution, or a build system. It just needs to be readable by an agent.

Forges solve this by making knowledge portable: clone the repo, copy the skills, invoke them. No install step. No runtime. No maintenance burden.

## forge-forge's Responsibility

1. **Define the standard** — what structure, files, and guardrails every forge must have
2. **Create new forges** — `/forge-init` stamps out the standard structure
3. **Validate forges** — `/forge-audit` checks compliance
4. **Registry** — `registry.yaml` is the canonical list of all forges

## Success Metric

Every forge in the ecosystem passes `/forge-audit`. New forges are created via `/forge-init` and automatically registered.

