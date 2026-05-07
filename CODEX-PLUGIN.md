# Forge-Forge Codex Plugin

Forge-Forge is an Eidos AGI Codex plugin that tells Codex to use the canonical forge registry, CLI, and MCP tools for forge discovery and forge-pattern work.

## Eidos AGI Plugin Family

- `rhea@eidos-agi`: sovereign model routing, debate, pairing, and image tools.
- `foreman@eidos-agi`: multi-agent coding delegation and git worktree execution.
- `reeves@eidos-agi`: routing layer for the live Reeves CLI.
- `surfari@eidos-agi`: routing layer for the live Surfari CLI and browser-agent improvement loop.
- `forge-forge@eidos-agi`: routing layer for Eidos forge discovery and forge creation patterns.

## Install In Codex

Clone the repo:

```bash
mkdir -p /Users/dshanklinbv/repos-eidos-agi
git clone git@github.com:eidos-agi/forge-forge.git /Users/dshanklinbv/repos-eidos-agi/forge-forge
```

Install or refresh the Eidos AGI Codex plugin cache:

```bash
mkdir -p /Users/dshanklinbv/.codex/plugins/cache/eidos-agi/forge-forge/0.2.0
rsync -a --delete --exclude '.git' --exclude '__pycache__' --exclude '.venv' \
  /Users/dshanklinbv/repos-eidos-agi/forge-forge/ \
  /Users/dshanklinbv/.codex/plugins/cache/eidos-agi/forge-forge/0.2.0/
```

Add Forge-Forge to `~/.agents/plugins/marketplace.json`:

```json
{
  "name": "forge-forge",
  "source": {
    "source": "local",
    "path": "./plugins/forge-forge"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Productivity"
}
```

Enable the plugin and MCP server in `~/.codex/config.toml`:

```toml
[plugins."forge-forge@eidos-agi"]
enabled = true

[mcp_servers.forge_forge]
transport = "stdio"
command = "/Users/dshanklinbv/repos-eidos-agi/forge-forge/.venv/bin/forge-forge-mcp"
args = []
tool_timeout_sec = 600
```

Restart Codex after editing config.

## Smoke Test

```bash
cd /Users/dshanklinbv/repos-eidos-agi/forge-forge
.venv/bin/forge list
.venv/bin/forge find "create a company cleanup repo"
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
  | .venv/bin/forge-forge-mcp
```
