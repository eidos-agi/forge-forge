---
id: PLAN-0001
title: Forge Discovery + Provenance — make forges a first-class installable concept
status: draft
created: '2026-04-02'
tags:
  - architecture
  - mcp
  - manifest
verification:
  - Agent in a fresh cockpit can ask forge-forge MCP 'how do I use improve-forge?' and
  get actionable answer
  - After running /loss-init on a project, .forge/installed.yaml records loss-forge
  with date and artifacts
  - CLAUDE.md template references .forge/ for ecosystem discovery
  - cockpit grade includes an L7 checking forge provenance freshness
---
# Forge Discovery + Provenance

## Problem

An agent lands in a project and can't find forges. The wrike-ops transcript proves it: agent had improve-forge available but couldn't discover it. Meanwhile, forges that HAVE been run on a project leave artifacts (loss.py, CONTRIBUTING.md, CI workflows) but nothing records that the forge was the source.

Two gaps:
1. **Discovery**: "What forges exist and how do I use them?" — needs to be answerable from any session
2. **Provenance**: "Which forges have already been applied to this project?" — needs to be recorded per-project

## Design

### Part 1: Enhance forge-forge MCP server (Discovery)

The MCP server already exists with `forge_find`, `forge_list`, `forge_info`. What's missing:

**A. `forge_how` tool** — Given a forge name, return actionable invocation instructions. Not just "these skills exist" but "here's how to use them right now." This is the tool that would have answered the wrike-ops agent.

```python
@mcp.tool()
def forge_how(name: str) -> dict:
    """How to use a specific forge — invocation, prerequisites, expected artifacts."""
```

Returns:
- Prerequisites (is it cloned locally? is it an MCP server? does it need pip install?)
- Invocation instructions (skill names, CLI commands, MCP tool names)
- Expected artifacts (what files/dirs does this forge create when run?)
- Example usage (one-liner showing the most common invocation)

This requires enriching `registry.yaml` with new fields per forge:
```yaml
- name: loss-forge
  invocation: skill          # skill | mcp | cli
  prerequisites:
    clone: true              # must be cloned locally for skills
    pip: false               # no pip install needed
  artifacts:
    - loss.py                # files it creates
    - LOSS-BASELINE.md
  example: "/loss-init"
```

**B. `forge_for_project` tool** — Given a project path or description, recommend which forges should be applied.

```python
@mcp.tool()
def forge_for_project(path: str = "", description: str = "") -> dict:
    """Recommend forges for a project based on its characteristics."""
```

Reads the project's pyproject.toml, CLAUDE.md, file structure to determine:
- Is it a PyPI package? → foss-forge, ship-forge
- Is it an MCP server? → ship-forge (ship-qa)
- Does it have tests? → test-forge
- Does it deploy? → ship-forge (ship-deploy)
- Does it have loss functions? → loss-forge (already installed) or (needs /loss-init)
- Is it public? → security-forge, foss-forge

Cross-references against `.forge/installed.yaml` (Part 2) to show what's installed vs recommended.

### Part 2: Forge Provenance (per-project installed.yaml)

When a forge acts on a project, it stamps `.forge/installed.yaml`:

```yaml
# .forge/installed.yaml — Forges that have been applied to this project
forges:
  loss-forge:
    installed: 2026-04-02
    version: "0.1.0"            # forge version at time of install (if available)
    artifacts:
      - src/ai_cockpit/loss.py
      - LOSS-BASELINE.md
    skill_used: /loss-init
    
  foss-forge:
    installed: 2026-04-01
    artifacts:
      - CONTRIBUTING.md
      - LICENSE
    skill_used: /foss-init
```

**Who writes this file?** Each forge's init skill should append to it. This means updating:
- loss-forge's `/loss-init` skill — add a step: "append to .forge/installed.yaml"
- foss-forge's `/foss-init` skill — same
- ship-forge's `/ship-init` skill — same
- security-forge's `/sec-audit` skill — same
- Any forge that creates artifacts in a project

**Convention, not enforcement.** Forges that don't stamp are still fine. The file is append-only, never required. But forges that DO stamp make the next agent's job easier.

### Part 3: Wire into CLAUDE.md template

The cockpit template's CLAUDE.md should reference `.forge/installed.yaml`:

```markdown
## Forge Ecosystem

This project participates in the Eidos forge ecosystem. 
See `.forge/installed.yaml` for forges that have been applied.
Use the forge-forge MCP server to discover available forges:
- `forge_find("what forges help with X?")`
- `forge_how("loss-forge")`
- `forge_for_project(path=".")`
```

### Part 4: Manifest spec v2 — add forges section

Extend `spec/manifest-v1.yaml` → `manifest-v2.yaml` with:

```yaml
# --- forges (enforced by forge-forge) ---
forges:
  installed: .forge/installed.yaml    # path to provenance file
  recommended:                         # forges that SHOULD be applied
    - loss-forge                       # every project should have loss functions
    - foss-forge                       # if public
    - security-forge                   # if public or deployed
  optional:                            # nice-to-have
    - improve-forge
    - demo-forge
```

`forge-enforce` then checks: "manifest says loss-forge is recommended, is it in installed.yaml?"

## Task Breakdown

1. **Enrich registry.yaml** — add invocation, prerequisites, artifacts, example per forge
2. **Add `forge_how` tool** to MCP server
3. **Add `forge_for_project` tool** to MCP server
4. **Define `.forge/installed.yaml` spec** — format, conventions, who writes it
5. **Update loss-forge /loss-init** — stamp installed.yaml after running
6. **Update ai-cockpit template CLAUDE.md** — reference forge ecosystem
7. **Update manifest spec** — v2 with forges section
8. **Test** — run forge_how("improve-forge") and verify the wrike-ops scenario is solved

## Order of Operations

1 → 2 → 8 (test the discovery fix first — highest value)
Then 4 → 5 → 3 → 6 → 7 (provenance, then recommendations, then wiring)

## What This Does NOT Include

- docs-forge (overkill, covered by existing forges)
- Automated forge installation (forges are skills, not packages — "install" means "clone and use")
- Fleet-wide forge enforcement (that's cockpit's job, not forge-forge's)
