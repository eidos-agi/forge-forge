# forge-sync — Ensure All Forges Are Cloned Locally

Check which registered forges are cloned locally and provide clone commands for any that are missing.

## Trigger

User says `/forge-sync` or asks to sync, clone, or set up all forges locally.

## Instructions

1. Read the forge registry at `~/repos-eidos-agi/forge-forge/registry.yaml`
2. For each forge, check if `~/repos-eidos-agi/<name>/` exists
3. Report status and provide clone commands for missing forges

## Output Format

```
## Forge Sync Status

| Forge | Local | Path |
|-------|-------|------|
| foss-forge | ✓ | ~/repos-eidos-agi/foss-forge |
| demo-forge | ✓ | ~/repos-eidos-agi/demo-forge |
| forge-forge | ✓ | ~/repos-eidos-agi/forge-forge |
| test-forge | ✗ | not cloned |

### Clone missing forges:

git clone https://github.com/eidos-agi/test-forge.git ~/repos-eidos-agi/test-forge
```

If all forges are cloned:
```
All 4 forges are cloned locally. Ecosystem is in sync.
```

## Rules

- Read-only. Don't clone anything automatically — just provide the commands.
- Check existence with a simple directory check, not git status.
- If registry.yaml doesn't exist, tell the user to clone forge-forge first.
