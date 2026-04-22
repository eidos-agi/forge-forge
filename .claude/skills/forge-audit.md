# forge-audit — Audit a Forge Against the Forge Standard

Check whether a repo meets the Forge Standard — the structural and quality requirements for an Eidos AGI forge.

## Trigger

User says `/forge-audit` or asks to validate, audit, or check a forge.

## Instructions

Run every check below against the current working directory. Report PASS, FAIL, or WARN for each.

### Structure Checks

| Check | Criteria |
|-------|---------|
| `.claude/skills/` exists | Directory present with at least one `.md` skill file |
| `templates/` exists | Directory present (may be empty for new forges) |
| `.visionlog/` exists | Initialized with config.yaml |
| `CLAUDE.md` exists | Present, >10 lines |
| `README.md` exists | Present, >20 lines |
| `LICENSE` exists | Present, contains recognized license |

### Anti-Patterns (should NOT exist)

| Check | Criteria |
|-------|---------|
| No `pyproject.toml` | Forges are not software. FAIL if present. |
| No `setup.py` | FAIL if present |
| No `package.json` | FAIL if present |
| No `src/` directory | WARN if present — forges don't have source code |
| No `Dockerfile` | WARN if present — forges don't get deployed |

### Visionlog Quality

| Check | Criteria |
|-------|---------|
| Vision set | `.visionlog/vision.md` exists and is non-empty |
| Guardrails exist | At least one guardrail, including "no software" |
| "No software" guardrail | A guardrail explicitly prohibiting installable software exists |
| Goals exist | At least one goal defined |

### Skill Quality

For each `.md` file in `.claude/skills/`:

| Check | Criteria |
|-------|---------|
| Has Trigger section | Skill defines when it activates |
| Has Instructions section | Skill has clear step-by-step instructions |
| Has Rules section | Skill defines constraints and boundaries |
| Reasonable length | WARN if >300 lines (skills should be focused) |

### README Quality

| Check | Criteria |
|-------|---------|
| Usage instructions | README explains how to install/use the skills (clone + copy pattern) |
| Skills table | README has a table listing all skills with descriptions |

### Registry Consistency

| Check | Criteria |
|-------|---------|
| Registered | This forge appears in `~/repos-eidos-agi/forge-forge/registry.yaml` |
| Skills match files | Every skill listed in registry.yaml for this forge has a corresponding `.md` file in `.claude/skills/`. WARN if registry lists skills that don't exist as files (registry drift). |
| Files match registry | Every `.md` file in `.claude/skills/` is listed in registry.yaml. WARN if orphan skills exist. |

### Git Hygiene

| Check | Criteria |
|-------|---------|
| Default branch is `main` | `git symbolic-ref --short HEAD` returns `main`. FAIL on `master` or other — ecosystem convention is `main`. (INC-005) |
| Has GitHub remote | `git remote get-url origin` returns `eidos-agi/<forge-name>`. FAIL if missing — vision-only scratch is not a forge. (INC-003) |
| Working tree not behind upstream | `git fetch && git rev-list --count HEAD..@{u}` returns 0. WARN otherwise — editing a stale working tree causes merge collisions. (INC-001) |
| No generic "sync working state" commits ahead of upstream | `git log @{u}..HEAD --format=%s` contains no "chore: sync working state" or similar content-free messages. WARN if found. (INC-004) |

### Registry Syntax (forge-forge only)

When auditing forge-forge itself:

| Check | Criteria |
|-------|---------|
| registry.yaml parses | `python -c "import yaml; yaml.safe_load(open('registry.yaml'))"` exits 0. FAIL otherwise — a broken registry poisons every `forge_find`, `forge_info`, `forge_how` call. (INC-006) |
| Every entry has required fields | Each entry has `name`, `type`, `description`, `repo`, `invocation`, `prerequisites`. FAIL if any missing. |
| No duplicate names | No two entries share a `name`. FAIL if duplicates exist. |

## Output Format

```
## Forge Audit: <forge-name>

| # | Category | Check | Status | Detail |
|---|----------|-------|--------|--------|
| 1 | Structure | .claude/skills/ | PASS | 3 skills found |
| 2 | Structure | templates/ | PASS | 8 templates |
| 3 | Anti-pattern | No pyproject.toml | PASS | Not present |
| 4 | Visionlog | Vision set | PASS | "foss-forge — Make Agentic Software..." |
| ... | ... | ... | ... | ... |

### Verdict: VALID FORGE (15/16 checks passed)

### Issues
1. **Not registered** — Add to forge-forge/registry.yaml
```

## Rules

- Read-only. Don't create or modify files.
- If the repo has a pyproject.toml, it's not a forge — say so clearly.
- Check the registry by reading `~/repos-eidos-agi/forge-forge/registry.yaml`.
