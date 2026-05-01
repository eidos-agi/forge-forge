---
name: forge
description: Agent-first CLI for the Eidos forge ecosystem. Use this CLI to find, list, inspect, and invoke forges — costs zero tokens until invoked. Replaces the forge-forge MCP for most use cases.
user_invocable: true
---

# forge — find, list, inspect Eidos forges

Agent-first CLI generated per the cli-forge contract. The MCP server
(`forge-forge-mcp`) is still available for in-Claude-Code tool surfacing,
but the CLI is cheaper and more composable. All commands support `--json`
and `--quiet`. `--help` is the authoritative schema.

## Trigger

Use this CLI when you need to:
- Find a forge for a task (`forge find "test my API"`).
- List forges in the ecosystem (`forge list`, `forge list --type tool`).
- Inspect a specific forge (`forge info ml-forge`).
- Get invocation steps (`forge how cli-forge`).
- Recommend forges for a project (`forge for-project --path .`).

Reach for `forge` before the `forge-forge` MCP — it costs zero context
tokens until invoked.

## Setup

No environment variables required. The CLI reads `registry.yaml` from
the forge-forge install location at module import time.

## Commands

```
forge                              # progressive reveal — list available commands
forge find QUERY [--top-k N] [--json] [--quiet]
forge list [--type knowledge|tool] [--json] [--quiet]
forge info NAME [--json] [--quiet]
forge how NAME [--json] [--quiet]
forge for-project [--path PATH] [--description TEXT] [--json] [--quiet]
```

Run `forge <command> --help` for full schema.

## Discovery

`forge` with no arguments is identical to `forge --help`. One discovery
surface, no separate banner. The CLI does one thing: tell you to use
the CLI and list the main commands.

- **`forge`** = **`forge --help`** — full schema and command list, exit 0.
- **`forge <typo>`** = `Error: unknown command 'X'. Did you mean 'find'?`, exit 2.
- **`forge <command> --help`** = authoritative schema for that subcommand.

## Canonical Workflows

### Find the right forge for a task and read its details

```bash
match=$(forge find "test my API" --json | jq -r '.matches[0].name')
forge info "$match" --json | jq
```

### Recommend forges for the project I'm in

```bash
forge for-project --json | jq '.recommended[] | select(.installed == false)'
```

### Pipe forge names into other tools

```bash
forge list --quiet | grep -i forge | xargs -n1 forge info --quiet
```

## Safety

- All data is read-only. The CLI never modifies the registry, never
  installs forges, never clones repos. Use `forge how NAME` to get the
  ready-to-run installation steps; execute them yourself.

## Rules for Agents

- **Always use `--json`** unless piping one value to another command — then `--quiet`.
- **`forge info` and `forge how` exit 2 on unknown name** with a `did_you_mean`
  field in JSON output. Use it.
- **`forge` with no args is fine** — it's the discovery surface, not an error.
- **`--help` is ground truth.** If this skill mentions a flag that `--help`
  does not, the skill is stale.
- **One command per step.** Read each JSON result before deciding the next.
