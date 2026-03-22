# forge-enforce — Enforce Manifest Desired State

Read a repo's `.forge/manifest.yaml`, compare it to reality, and report drift. Optionally fix drift with user approval.

## Trigger

User says `/forge-enforce` or asks to enforce, check drift, validate manifest, or verify repo state against its declared config.

## Instructions

### Step 1: Load Manifest

1. Read `.forge/manifest.yaml` in the current repo. If missing, offer to scaffold one via `/forge-manifest-init`.
2. Read the centralized baseline at `~/repos-eidos-agi/forge-forge/defaults/baseline.yaml`.
3. **Merge**: repo-local manifest overrides baseline. Missing sections in local = use baseline defaults.
4. Validate `manifest_version` — currently only `1` is supported.

### Step 2: Observe Reality

For each section in the merged manifest, gather the actual state:

#### repo section
- `visibility`: Run `gh repo view {org}/{repo} --json visibility` or check GitHub API
- `topics`: Run `gh repo view {org}/{repo} --json repositoryTopics`
- `org`: From `git remote get-url origin`

#### packaging section
- `build_system`: Read `pyproject.toml` `[build-system]` → `build-backend`
- `pypi.name`: Read `pyproject.toml` `[project]` → `name`
- `pypi.publish`: Check if package exists on PyPI (`pip index versions {name}`)
- `pypi.trusted_publisher`: Read `.github/workflows/publish.yml` — check for `id-token: write`, `environment: pypi`, `pypa/gh-action-pypi-publish`
- `readme.absolute_images`: Grep README.md for `<img src="` and `![](` with relative paths

#### quality section
- `required_files`: Check each file exists with `test -f`
- `min_grade`: Run the relevant forge check mentally or reference last audit results

#### security section
- `secret_scanning`: Grep for secret patterns (delegate to `/sec-scan` logic)
- `dependency_audit`: Check if `pip-audit` would pass
- `git_history_scan`: Check git history for secret file patterns

#### deployment section (if present)
- `health_check`: Grep source for the declared endpoint path
- `env_documented`: Check `.env.example` exists
- `graceful_shutdown`: Grep for SIGTERM/signal handling

#### dependencies section
- `max_count`: Count `project.dependencies` in pyproject.toml
- `banned`: Check if any banned dep appears in dependencies
- `heavy_warning`: Check if any heavy dep appears

#### ci section
- `workflows.ci`: Check `.github/workflows/ci.yml` exists
- `workflows.publish`: Check `.github/workflows/publish.yml` exists
- `permissions.contents_read`: If publish workflow sets explicit permissions, check `contents: read` is included
- `pre_commit`: Check `.pre-commit-config.yaml` exists
- `build_verification`: Check if CI workflow includes install-test step

### Step 3: Generate Plan (the diff)

Compare desired state (manifest) to observed state (reality). For each field:

| Status | Meaning |
|--------|---------|
| `OK` | Reality matches manifest |
| `DRIFT` | Reality differs from manifest — needs fix |
| `UNKNOWN` | Cannot verify (e.g., no GitHub API access, PyPI unreachable) |
| `EXCEPTION` | Drift exists but covered by a valid exception (not expired) |

### Step 4: Check Exceptions

For each `DRIFT` item, check the `exceptions` array in the manifest:
- If a matching exception exists AND `expires` is in the future → mark as `EXCEPTION`
- If a matching exception exists AND `expires` is in the past → mark as `DRIFT` and note "exception expired"
- Exceptions require `justification`, `owner`, and `expires`

### Step 5: Output the Plan

```
## Forge Enforce: {repo-name}

Manifest: .forge/manifest.yaml (v1)
Baseline: forge-forge/defaults/baseline.yaml
Merged fields: {N} from manifest, {M} from baseline

### Plan

| # | Section | Field | Desired | Actual | Status |
|---|---------|-------|---------|--------|--------|
| 1 | repo | visibility | public | private | DRIFT |
| 2 | packaging | build_system | hatchling | hatchling | OK |
| 3 | packaging | readme.absolute_images | true | false (3 relative) | DRIFT |
| 4 | quality | LICENSE | required | exists | OK |
| 5 | quality | CHANGELOG.md | required | missing | DRIFT |
| 6 | ci | pre_commit | true | false | DRIFT |
| 7 | dependencies | max_count | 5 | 4 | OK |
| 8 | dependencies | banned.numpy | banned | not present | OK |

### Summary: 4 DRIFT, 8 OK, 0 EXCEPTION, 0 UNKNOWN

### Drift Details

1. **repo.visibility**: DRIFT — manifest says `public`, repo is `private`
   → Fix: `gh repo edit {org}/{repo} --visibility public`
   ⚠️ HIGH RISK — changing visibility is irreversible for private→public

2. **packaging.readme.absolute_images**: DRIFT — 3 relative image paths found
   → Fix: Replace `src="logo.png"` with `src="https://raw.githubusercontent.com/{org}/{repo}/main/logo.png"`

3. **quality.CHANGELOG.md**: DRIFT — file missing
   → Fix: Run `/foss-init changelog`

4. **ci.pre_commit**: DRIFT — .pre-commit-config.yaml missing
   → Fix: Run `/ship-init precommit`
```

### Step 6: Apply (with approval)

After showing the plan, ask the user:
```
4 items need fixing. Apply all? [y/n/select]
```

- `y` — fix all non-destructive items. For HIGH RISK items (visibility changes, branch protection), ask individually.
- `n` — report only, don't fix anything.
- `select` — let user choose which items to fix.

For each fix:
- **File creation** (CHANGELOG, .pre-commit-config): create from templates
- **File edits** (absolute images, pyproject.toml): edit directly
- **GitHub settings** (visibility, topics): use `gh` CLI
- **HIGH RISK changes**: always ask individually, never batch

## Rules

- **Plan is always safe.** Reading state and showing the diff never modifies anything.
- **Apply requires explicit approval.** Never auto-apply.
- **HIGH RISK items get individual approval.** Visibility changes, branch protection, anything that affects access.
- **Idempotent.** Running enforce twice produces the same plan if nothing changed.
- **Expired exceptions are not valid.** Treat them as DRIFT and flag the expiry.
- **If no manifest exists**, offer to create one — don't just fail.
- **If `gh` CLI is not available** for GitHub checks, mark those as UNKNOWN and suggest manual verification.
