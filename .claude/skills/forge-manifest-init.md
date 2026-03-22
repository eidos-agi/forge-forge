# forge-manifest-init — Scaffold a .forge/manifest.yaml

Generate a `.forge/manifest.yaml` for the current repo by reading its actual state and declaring it as desired state.

## Trigger

User says `/forge-manifest-init` or asks to create a manifest, set up forge enforcement, or declare repo desired state.

## Instructions

### Step 1: Read Current State

Gather everything about the repo:

1. **Git remote** → extract org and repo name
2. **pyproject.toml** → package name, version, build system, dependencies, entry points
3. **GitHub** → visibility (via `gh repo view` if available), topics
4. **Existing files** → LICENSE, CHANGELOG, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY.md, .pre-commit-config.yaml
5. **CI workflows** → .github/workflows/*.yml
6. **Deployment** → Dockerfile, Procfile, Railway config, health check endpoints in source

### Step 2: Determine Project Type

| Signal | Type |
|--------|------|
| `mcp.server`, `FastMCP`, `@mcp.tool` in source | MCP server |
| `[project.scripts]` with CLI entry points | CLI tool |
| No entry points, just a package | Library |
| `.visionlog/` + `.claude/skills/` + no pyproject.toml | Knowledge forge |

### Step 3: Generate Manifest

Create `.forge/manifest.yaml` with the current state as desired state, plus recommended improvements.

For each section:
- **If the state is good** → declare it (e.g., `visibility: public` if already public)
- **If the state is missing** → declare the recommended default from baseline
- **Add comments** explaining non-obvious fields

### Step 4: Show and Confirm

Display the generated manifest to the user. Ask:
```
This declares your repo's desired state. Review it:
- Anything to change before saving?
- Any exceptions needed?
```

### Step 5: Write

Create `.forge/manifest.yaml` in the repo root.

## Output

A complete, valid `.forge/manifest.yaml` that can be immediately enforced with `/forge-enforce`.

## Rules

- **Never overwrite** an existing `.forge/manifest.yaml`. If one exists, show it and offer to update specific sections.
- **Declare reality, then improve.** Start with what IS true, add what SHOULD be true. Don't set aspirational goals without noting them as drift-to-fix.
- **Ask before writing.** Show the full manifest for review first.
- **Include comments.** This file will be read by humans reviewing PRs that change policy.
