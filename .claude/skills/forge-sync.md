---
name: forge-sync
description: Three-way reconciliation of the forge ecosystem — registry vs GitHub org vs local filesystem. Surfaces orphans, drift, and missing clones.
---

# forge-sync — Ecosystem Reconciliation

Keep the forge ecosystem honest. At launch, confirm three sources agree:

1. **Registry** — `~/repos-eidos-agi/forge-forge/registry.yaml` (the declared truth)
2. **GitHub** — all `*-forge` repos under `eidos-agi/` (the public truth)
3. **Local** — directories under `~/repos-eidos-agi/*-forge/` (the working truth)

## Trigger

User says `/forge-sync`, asks to sync forges, asks "are we tracking all the forges?", or is doing launch-time situational awareness on the forge ecosystem.

## Instructions

Run the four probes in parallel, then reconcile.

### 1. Load registry

```bash
cat ~/repos-eidos-agi/forge-forge/registry.yaml
```

Extract the `name:` field of every entry under `forges:`.

### 2. List GitHub forges

```bash
gh repo list eidos-agi --limit 200 --json name,pushedAt,isArchived,isEmpty \
  --jq '.[] | select(.name | endswith("-forge")) | "\(.name)\t\(.pushedAt)\t\(.isArchived)\t\(.isEmpty)"'
```

Skip archived repos. Flag empty repos as "placeholder" (don't register until they have content).

### 3. List local forge directories

```bash
ls -1d ~/repos-eidos-agi/*-forge 2>/dev/null | xargs -n1 basename
```

### 4. Per-forge drift check (for forges that are both registered AND cloned)

For each intersection entry, run:

```bash
cd ~/repos-eidos-agi/<name> && git fetch --quiet 2>/dev/null && \
  branch=$(git symbolic-ref --short HEAD 2>/dev/null || echo "?") && \
  dirty=$(git status --porcelain=v1 2>/dev/null | wc -l | tr -d ' ') && \
  ab=$(git rev-list --left-right --count "$branch"...@{u} 2>/dev/null | tr '\t' '/' || echo "?/?") && \
  echo "$branch ahead/behind:$ab dirty:$dirty"
```

Flag anything that shows `ahead`, `behind`, uncommitted changes, a missing upstream, or a branch other than `main`.

## Reconciliation Output

Produce three tables, then a plan.

### Table 1 — Reconciliation Matrix

| Forge | Registry | GitHub | Local | Status |
|-------|----------|--------|-------|--------|
| test-forge | ✓ | ✓ | ✓ | ✅ in sync |
| nightingale-forge | ✗ | ✓ | ✗ | ⚠ online-only, orphan |
| adr-forge | ✗ | ✗ | ✓ | ⚠ local-only scratch |
| ship-forge | ✓ | ✓ | ✗ | ⚠ registered but not cloned |

Use ✅ only when all three columns are ✓ AND the local working tree is clean, on `main`, and in sync with origin.

### Table 2 — Drift Report (for cloned forges)

| Forge | Branch | Ahead/Behind | Dirty | Last Push |
|-------|--------|--------------|-------|-----------|
| forge-forge | main | 0/0 | no | 2026-04-22 |
| brand-forge | main | 1/1 | no | 2026-03-31 |

Callouts: non-`main` default branch, divergence (both ahead and behind), dirty trees, no upstream.

### Table 3 — Unregistered Discoveries

Split orphans into actionable tiers:

- **Online, legit, worth registering** — has README + skills/tools + recent pushes + not empty. Propose a registry entry (draft the YAML block).
- **Online, empty placeholder** — GitHub repo exists but `isEmpty: true`. Note it, don't register. Revisit when content lands.
- **Local, has content** — has `.claude/skills/` or meaningful files but no GitHub repo. Ask the user: ship it to GitHub, or is this private scratch?
- **Local, vision-only** — has `.visionlog/` but no skills, no git repo. Flag as "scoped but unbuilt." Don't register.
- **Archived or stale** — skip but note it.

## Action Plan

End the report with concrete next steps, ordered by reversibility:

1. **Register the safe ones** — if an online orphan has content and skills, offer to append a registry entry and commit.
2. **Clone the missing ones** — print `gh repo clone eidos-agi/<name> ~/repos-eidos-agi/<name>` for each registered-but-not-cloned forge.
3. **Resolve drift** — for dirty or diverged clones, name the forge and suggest `/land`-style action. Don't auto-push or auto-merge.
4. **Decide on local scratch** — ask before touching anything that looks like in-progress work (especially `.visionlog/`-only directories).

## Rules

- **Always pull registry changes first** — `cd ~/repos-eidos-agi/forge-forge && git fetch && git pull --ff-only` before editing `registry.yaml`. Another session may have added forges.
- **Read-mostly at launch.** Only edit `registry.yaml` if the user says go. Never clone automatically. Never touch a foreign working tree.
- **Never delete local scratch.** A `.visionlog/`-only directory is a vision someone scoped — ask before suggesting removal.
- **One fetch per forge.** Don't recurse or call `git pull`. A fetch + status is enough to detect drift.
- **If `registry.yaml` doesn't exist**, tell the user to clone `forge-forge` first.
- **If the user is offline** (gh fails), fall back to a two-way reconciliation (registry vs local) and note that the GitHub side is stale.
