# forge-catalog — List All Forges in the Ecosystem

Display the complete registry of Eidos AGI forges with their skills, descriptions, and status.

## Trigger

User says `/forge-catalog` or asks to list, show, or browse available forges.

## Instructions

1. Read the forge registry at `~/repos-eidos-agi/forge-forge/registry.yaml`
2. For each forge:
   - Count the number of skills listed
   - Check if cloned locally (does `~/repos-eidos-agi/<name>/` exist?)
   - Display in a summary table
3. Show total skill count across the ecosystem

## Output Format

```
## Eidos AGI Forge Ecosystem

| Forge | Description | Skills | Local | GitHub |
|-------|------------|--------|-------|--------|
| foss-forge | Open-source standards and marketing | 5 skills | ✓ | eidos-agi/foss-forge |
| demo-forge | AI-generated demo content | 2 skills | ✓ | eidos-agi/demo-forge |
| forge-forge | Meta-forge for creating forges | 3 skills | ✓ | eidos-agi/forge-forge |
| test-forge | Testing standards | 5 skills | ✓ | eidos-agi/test-forge |

### Skills by Forge

**foss-forge** — Open-source standards and marketing for agentic software
- /foss-check — audit a repo against FOSS standards
- /foss-init — scaffold missing community health files
- /foss-release — guided PyPI release
- /foss-launch — marketing playbook
- /foss-demo — demo assessment (delegates to demo-forge)

**demo-forge** — AI-generated demo content
- /demo — generate demos (GIFs, SVGs, screenshots, diagrams)
- /demo-audit — assess demo quality

...
```

## Rules

- Read-only. Just display information.
- If registry.yaml doesn't exist, tell the user to create it or run `/forge-init` first.
- Check local presence with a simple directory existence check, not git status.
