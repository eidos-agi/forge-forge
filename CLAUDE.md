# CLAUDE.md — forge-forge

> The forge that forges forges. Meta-forge for creating and managing the Eidos AGI forge ecosystem.

## What This Is

forge-forge owns the **Forge Standard** — what a forge IS, how to create one, how to validate one, and the canonical registry of all forges.

## What is a Forge?

A forge is a repo that packages **reusable agent knowledge** as Claude Code skills and templates. No software. No CLI. No package. Just knowledge that agents use to do specialized work.

Every forge follows the same structure:
```
<forge-name>/
├── .claude/skills/    ← agent skills (markdown)
├── .visionlog/        ← vision, goals, guardrails
├── templates/         ← parameterized file templates
├── CLAUDE.md          ← project instructions
├── README.md          ← public docs
└── LICENSE            ← MIT
```

Every forge has the "no software" guardrail. Every forge has a vision. Every forge is public.

## Skills

| Skill | What It Does |
|-------|-------------|
| `/forge-init` | Scaffold a new forge with visionlog, guardrails, skills dir, templates, GitHub repo |
| `/forge-audit` | Audit a repo against the Forge Standard — structure, visionlog, anti-patterns |
| `/forge-catalog` | List all forges in the ecosystem from the registry |
| `/forge-sync` | Check which forges are cloned locally, provide clone commands for missing ones |

## Registry

`registry.yaml` is the canonical list of all Eidos AGI forges. Updated by `/forge-init` when new forges are created.

## Related Forges

- **foss-forge** — open-source standards and marketing for agentic software
- **demo-forge** — AI-generated demos (GIFs, SVGs, screenshots, diagrams)
- **security-forge** — security auditing and agentic threat modeling
- **test-forge** — testing standards and test generation
