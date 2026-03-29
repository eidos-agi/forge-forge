# Proposal: Reorganize forges around contracts, not skills

## Learning
Skills are scaffolding for current models. Contracts are durable infrastructure for all models. The forge system should be organized around contracts first, skills second.

## Source
eidos-assistant build session (2026-03-29). After building 3 forges and running them on real projects, realized: the data schemas (improvement snapshots, proposals, buckets, learning logs) are the permanent value. The skills that produce them are temporary.

## Proposed Change
- **Target:** forge-forge standard (affects all forges)
- **Change:** Every forge must define its contracts in a `contracts/` directory using JSON Schema. Skills reference contracts but contracts don't reference skills. The forge standard becomes:

```
<forge-name>/
  contracts/           ← THE DURABLE PART
    <name>.schema.json
    <name>.example.json
  .claude/skills/      ← scaffolding, references contracts
  templates/           ← may also reference contracts
  .visionlog/          ← governance
```

Forge-forge's audit should check: does every data output have a contract? Skills are optional scaffolding. Contracts are mandatory infrastructure.

## Why This Matters
1. Models improve. Skills become unnecessary. Contracts survive.
2. New agents read the schema and produce conforming output without needing the skill.
3. Contracts are validatable — you can check if output conforms. Skills are prose — you can only hope.
4. Cross-forge integration works through shared contracts, not shared skills.
5. This is Sutton-aligned: general infrastructure that scales with compute, not hand-crafted knowledge that doesn't.

## Evidence
This session produced 8 implicit contracts scattered across skill files, README prose, and Python dataclasses. None are formally defined. None are validatable. A new agent has to read 140 lines of improve.md to infer what a snapshot looks like.
