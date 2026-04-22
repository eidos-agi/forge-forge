---
name: forge-publish
description: Sync registry.yaml to eidosagi.com so the public /forges page always matches the registry. Also flags any forge that needs manual category placement.
---

# forge-publish — Push the Registry to the Website

Keeps the public forge list on [eidosagi.com/forges](https://eidosagi.com/forges) in sync with `registry.yaml`. Runs after adding, removing, or renaming a forge.

## Trigger

User says `/forge-publish`, asks to update the website, or has just edited `registry.yaml` and wants the public page current.

## Instructions

### Step 1: Confirm both repos are clean

```bash
cd ~/repos-eidos-agi/forge-forge && git status --porcelain && git pull --ff-only
cd ~/repos-eidos-agi/eidosagi.com && git status --porcelain && git pull --ff-only
```

Refuse to proceed if either has uncommitted changes that aren't explicitly the registry update.

### Step 2: Validate the registry

```bash
cd ~/repos-eidos-agi/forge-forge
python3 -c "import yaml; yaml.safe_load(open('registry.yaml'))"
.githooks/pre-commit || true   # belt and suspenders
```

Abort if the registry doesn't parse or fails schema checks.

### Step 3: Copy registry to the website data directory

```bash
cp ~/repos-eidos-agi/forge-forge/registry.yaml \
   ~/repos-eidos-agi/eidosagi.com/src/data/forges.yaml
```

That's the publish. The Astro build reads `src/data/forges.yaml` at build time via a `?raw` import in `src/lib/forges.ts`.

### Step 4: Diff and categorize new forges

```bash
cd ~/repos-eidos-agi/eidosagi.com
git diff src/data/forges.yaml | grep '^+.*- name:' | sed 's/^+  *- name: //'
```

For each new forge name, open `src/lib/forges.ts` and check if it appears in the `CATEGORIES` map. If not, add it — pick the category that best fits:

- `engineering` — forges that build, test, ship, or operate software
- `knowledge` — forges that produce content (writing, images, video, publishing)
- `business` — forges that do commerce, underwriting, marketing

If unsure, ask the user. Unmatched forges fall into an `other` bucket on the page.

### Step 5: Build locally to catch render errors

```bash
cd ~/repos-eidos-agi/eidosagi.com
npm install --no-audit --no-fund
npm run build
```

Verify no build errors. Spot-check the output:

```bash
grep -oE 'github\.com/eidos-agi/[a-z-]+' dist/client/forges/index.html | sort -u | wc -l
```

This should equal the forge count in the registry (`grep -c '^  - name:' src/data/forges.yaml`).

### Step 6: Commit and open a PR

Website changes land via PR, never direct push to main:

```bash
cd ~/repos-eidos-agi/eidosagi.com
BRANCH="chore/forge-publish-$(date +%Y%m%d-%H%M%S)"
git checkout -b "$BRANCH"
git add src/data/forges.yaml src/lib/forges.ts
git commit -m "chore: sync forge registry → eidosagi.com ($(date +%Y-%m-%d))"
git push -u origin "$BRANCH"
gh pr create --base main --head "$BRANCH" \
  --title "chore: sync forge registry" \
  --body "Refreshes src/data/forges.yaml from forge-forge/registry.yaml. New forges: <list>. See /forges preview."
```

## Output Format

```
## Forge Publish — <date>

Registry forges: <N>
Website forges (before): <M>
Delta: +<new> / -<removed>

### New forges to categorize
- <name>: currently falling into "other" — needs category in src/lib/forges.ts

### Build
- npm run build: PASS (Xs)
- forges rendered: <N>

### PR
- <PR URL>
```

## Rules

- **Registry is the source of truth.** The website's `src/data/forges.yaml` is a derived snapshot — never edit it directly. The `/forge-publish` skill is the only legitimate writer.
- **Always PR, never direct-push to main** on eidosagi.com. The site has real traffic; drift here is public.
- **Categorize before publishing.** A new forge in "other" on a public page is embarrassing; take the extra minute.
- **Run the build before opening the PR.** The `?raw` import means a broken YAML fails the build, not runtime — catch it locally.
- **Do not delete forges from the website without confirming they're actually gone from the ecosystem.** A forge disappearing from the page suggests it was killed; double-check before merging a removal.
